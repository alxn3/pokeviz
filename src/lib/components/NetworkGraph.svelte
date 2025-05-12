<!--https://observablehq.com/@d3/sticky-force-layout-->
<script lang="ts">
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import { type_colors } from '$lib/const';

  let { queried_pokemon } = $props();

  let svg, simulation;

  let container: HTMLDivElement;

  let width = $state(800);
  let height = $state(600);

  const margin = { top: 10, right: 30, bottom: 30, left: 40 };

  function clamp(x, min, max) {
    return Math.max(min, Math.min(max, x));
  }

  function getQueriedPokemonStats() {
    return Object.values(queried_pokemon).map((pokemon) => {
      const types = pokemon.types.sort((a, b) => a.slot - b.slot).map((t) => t.type.name);

      return {
        Name: pokemon.name,
        PrimaryType: types[0] || null,
        SecondaryType: types[1] || null,
      };
    });
  }

  let linksMap = {};

  function buildTypeGraph(pokemonList) {
    linksMap = {};
    const typeCounts = {};
    const typeSet = new Set();

    for (const pokemon of pokemonList) {
      const primary = pokemon.PrimaryType;
      const secondary = pokemon.SecondaryType;
      if (!primary) continue;

      typeCounts[primary] = (typeCounts[primary] || 0) + 1;
      typeSet.add(primary);
      if (secondary) typeSet.add(secondary);

      if (secondary) {
        typeSet.add(secondary);
        const key = [primary, secondary].sort().join('::');
        linksMap[key] = (linksMap[key] || 0) + 1;
      }
    }

    const typeToNodeId = {};
    let nextId = 0;
    const nodes = Array.from(typeSet).map((type) => {
      typeToNodeId[type] = nextId++;
      return { id: type, count: typeCounts[type] || 0 };
    });

    const links = [];
    for (const key in linksMap) {
      const [sourceType, targetType] = key.split('::');
      links.push({
        source: typeToNodeId[sourceType],
        target: typeToNodeId[targetType],
        weight: linksMap[key],
      });
    }

    return { nodes, links };
  }

  let hovered_id: string | null = $state(null);

  function renderGraph(graph) {
    // Clear previous layers
    svg.selectAll('.layer').remove();

    const link = svg
      .append('g')
      .attr('class', 'layer')
      .selectAll('line')
      .data(graph.links)
      .join('line')
      .attr('class', 'stroke-base-600/40')
      .attr('stroke-width', (d) => Math.sqrt(d.weight));

    const linkLabel = svg
      .append('g')
      .attr('class', 'layer')
      .selectAll('text')
      .data(graph.links)
      .join('text')
      .attr('class', 'text-base-800 font-semibold fill-current')
      .attr('text-anchor', 'middle')
      .attr('font-size', '0.75rem') // Tailwind text-xs
      .text((d) => d.weight);

    const node = svg
      .append('g')
      .selectAll('circle')
      .data(graph.nodes)
      .join('circle')
      .attr('r', 12)
      .attr('class', (d) => `layer stroke-type-500/40 stroke-2 fill-type-400 ${type_colors[d.id]}`)
      .classed('node', true)
      .classed('fixed', (d) => d.fx !== undefined)
      .call(d3.drag().on('start', dragstart).on('drag', dragged))
      .on('click', click)
      .on('mouseover', (event, d) => {
        hovered_id = d.id;
        node.attr('opacity', (n) => {
          const key = [n.id, d.id].sort().join('::');
          return n.id === d.id || linksMap[key] ? 1 : 0.3;
        });
        linkLabel.attr('opacity', (l) => (l.source.id === d.id || l.target.id === d.id ? 1 : 0));
        link.attr('opacity', (l) => (l.source.id === d.id || l.target.id === d.id ? 1 : 0.3));
        link.attr('stroke-width', (l) =>
          l.source.id === d.id || l.target.id === d.id ? l.weight : 1,
        );
        label.text((n) => {
          const key = [n.id, d.id].sort().join('::');

          const amt = d.id === n.id ? d.count : (linksMap[key] ?? 0);
          return `${n.id[0].toUpperCase() + n.id.slice(1)} (${amt})`;
        });
      })
      .on('mouseout', (event, d) => {
        hovered_id = null;
        node.attr('opacity', 1);
        linkLabel.attr('opacity', 1);
        link.attr('opacity', 1);
        link.attr('stroke-width', (l) => Math.sqrt(l.weight));
        label.text((n) => `${n.id[0].toUpperCase() + n.id.slice(1)} (${n.count})`);
      });

    const label = svg
      .append('g')
      .attr('class', 'layer')
      .selectAll('text')
      .data(graph.nodes)
      .join('text')
      .attr('class', 'text-base-900 font-semibold fill-current')
      .attr('text-anchor', 'middle')
      .attr('font-size', '0.75rem')
      .attr('dy', 20)
      .text((d) => `${d.id[0].toUpperCase() + d.id.slice(1)} (${d.count})`);

    simulation = d3
      .forceSimulation(graph.nodes)
      .force(
        'link',
        d3
          .forceLink(graph.links)
          .id((_, i) => i)
          .distance(200),
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .on('tick', ticked);

    function ticked() {
      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      node.attr('cx', (d) => d.x).attr('cy', (d) => d.y);

      label.attr('x', (d) => d.x).attr('y', (d) => d.y + 20);

      linkLabel
        .attr('x', (d) => (d.source.x + d.target.x) / 2)
        .attr('y', (d) => (d.source.y + d.target.y) / 2);
    }

    function dragstart(event, d) {
      d3.select(this).classed('fixed', true);
    }

    function dragged(event, d) {
      d.fx = clamp(event.x, 0, width);
      d.fy = clamp(event.y, 0, height);
      simulation.alpha(1).restart();
    }

    function click(event, d) {
      delete d.fx;
      delete d.fy;
      d3.select(this).classed('fixed', false);
      simulation.alpha(1).restart();
    }
  }

  let svggg;

  onMount(() => {
    width = container.clientWidth;
    height = container.clientHeight - 16;
    svggg = d3.select(container).append('svg').attr('width', width).attr('height', height);
    svg = svggg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);
  });

  $effect(() => {
    if (queried_pokemon && Object.keys(queried_pokemon).length > 0) {
      const typeData = getQueriedPokemonStats();
      const graph = buildTypeGraph(typeData);
      renderGraph(graph);
    }
  });
</script>

<div class="flex h-full flex-col gap-2">
  <p>Nodes numbers represent number of pokemon with corresponding primary type</p>
  <p>
    Edge numbers represent number of pokemon that have the both types of the nodes the edge connects
  </p>
  <div class="h-full overflow-hidden" bind:this={container}></div>
</div>

<svelte:window
  onresize={() => {
    width = container.clientWidth;
    height = container.clientHeight - 16;
    svggg.attr('width', width).attr('height', height);
    if (simulation) {
      simulation.force('center', d3.forceCenter(width / 2, height / 2));
      simulation.alpha(1).restart();
    }
  }}
/>
