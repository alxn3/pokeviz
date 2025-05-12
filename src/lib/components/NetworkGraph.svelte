<!--https://observablehq.com/@d3/sticky-force-layout-->
<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let queried_pokemon = {};

  let svg, simulation;
  const width = 800;
  const height = 800;
  const margin = { top: 10, right: 30, bottom: 30, left: 40 };

  function clamp(x, min, max) {
    return Math.max(min, Math.min(max, x));
  }

  function getQueriedPokemonStats() {
    return Object.values(queried_pokemon).map(pokemon => {
      const types = pokemon.types
        .sort((a, b) => a.slot - b.slot)
        .map(t => t.type.name);

      return {
        Name: pokemon.name,
        PrimaryType: types[0] || null,
        SecondaryType: types[1] || null
      };
    });
  }

  function buildTypeGraph(pokemonList) {
    const typeCounts = {};
    const typeSet = new Set();
    const linksMap = {};

    for (const pokemon of pokemonList) {
      const primary = pokemon.PrimaryType;
      const secondary = pokemon.SecondaryType;
      if (!primary) continue;

      typeCounts[primary] = (typeCounts[primary] || 0) + 1;
      typeSet.add(primary);
      if (secondary) typeSet.add(secondary);

      if (secondary) {
        typeSet.add(secondary)
        const key = [primary, secondary].sort().join('::');
        linksMap[key] = (linksMap[key] || 0) + 1;
      }
    }

    const typeToNodeId = {};
    let nextId = 0;
    const nodes = Array.from(typeSet).map(type => {

      typeToNodeId[type] = nextId++;
      return { id: type, count: typeCounts[type] || 0 };
    });

    const links = [];
    for (const key in linksMap) {
      const [sourceType, targetType] = key.split('::');
      links.push({
        source: typeToNodeId[sourceType],
        target: typeToNodeId[targetType],
        weight: linksMap[key]
      });
    }

    return { nodes, links };
  }

  function renderGraph(graph) {
    // Clear previous layers
    svg.selectAll(".layer").remove();

    const link = svg.append("g")
      .attr("class", "layer")
      .selectAll("line")
      .data(graph.links)
      .join("line")
      .attr("stroke", "#aaa")
      .attr("stroke-width", d => Math.sqrt(d.weight));

    const linkLabel = svg.append("g")
      .attr("class", "layer")
      .selectAll("text")
      .data(graph.links)
      .join("text")
      .attr("text-anchor", "middle")
      .attr("font-size", 10)
      .attr("fill", "#555")
      .text(d => d.weight);

    const node = svg.append("g")
      .attr("class", "layer")
      .selectAll("circle")
      .data(graph.nodes)
      .join("circle")
      .attr("r", 12)
      .attr("fill", "#69b3a2")
      .classed("node", true)
      .classed("fixed", d => d.fx !== undefined)
      .call(d3.drag()
        .on("start", dragstart)
        .on("drag", dragged))
      .on("click", click);

    const label = svg.append("g")
      .attr("class", "layer")
      .selectAll("text")
      .data(graph.nodes)
      .join("text")
      .attr("text-anchor", "middle")
      .attr("font-size", 10)
      .attr("dy", 20)
      .text(d => `${d.id} (${d.count})`);

    simulation = d3.forceSimulation(graph.nodes)
      .force("link", d3.forceLink(graph.links).id((_, i) => i).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .on("tick", ticked);

    function ticked() {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      label
        .attr("x", d => d.x)
        .attr("y", d => d.y + 20);

      linkLabel
        .attr("x", d => (d.source.x + d.target.x) / 2)
        .attr("y", d => (d.source.y + d.target.y) / 2);
    }

    function dragstart(event, d) {
      d3.select(this).classed("fixed", true);
    }

    function dragged(event, d) {
      d.fx = clamp(event.x, 0, width);
      d.fy = clamp(event.y, 0, height);
      simulation.alpha(1).restart();
    }

    function click(event, d) {
      delete d.fx;
      delete d.fy;
      d3.select(this).classed("fixed", false);
      simulation.alpha(1).restart();
    }
  }

  onMount(() => {
    svg = d3.select("#networkGraph")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);
  });

  $: if (queried_pokemon && Object.keys(queried_pokemon).length > 0 && svg) {
    const typeData = getQueriedPokemonStats();
    const graph = buildTypeGraph(typeData);
    renderGraph(graph);
  }
</script>

<style>
  #networkGraph {
    width: 100%;
    height: auto;
  }
</style>

<h2>Typing</h2>
<p>Nodes numbers represent number of pokemon with corresponding primary type<p/>
<p>Edge numbers represent number of pokemon that have the both types of the nodes the edge connects<p/>
<div id="networkGraph"></div>
