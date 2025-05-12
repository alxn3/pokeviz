<!-- Reference Code from 
  https://plotly.com/javascript/3d-scatter-plots/
  https://d3-graph-gallery.com/graph/scatter_basic.html 
-->

<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import { PCA } from 'ml-pca';
  import { draw } from 'svelte/transition';

  let { queried_pokemon } = $props();

  const statOptions = ['Total', 'HP', 'Attack', 'Defense', 'Sp.Atk', 'Sp.Def', 'Speed'];
  let selectedX1 = 'Speed';
  let selectedX = 'Attack';
  let selectedY = 'Speed';

  const margin = { top: 40, right: 30, bottom: 50, left: 60 },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

  let popularityData = [];
  let statData = [];

  function capitalizeFirst(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  function getQueriedPokemonStats() {
    return Object.values(queried_pokemon).map((pokemon) => {
      const statsMap = {
        Name: capitalizeFirst(pokemon.name),
        HP: 0,
        Attack: 0,
        Defense: 0,
        'Sp.Atk': 0,
        'Sp.Def': 0,
        Speed: 0,
        Total: 0,
      };

      for (const statEntry of pokemon.stats) {
        const rawName = statEntry.stat.name;
        const value = statEntry.base_stat;

        switch (rawName) {
          case 'hp':
            statsMap['HP'] = value;
            break;
          case 'attack':
            statsMap['Attack'] = value;
            break;
          case 'defense':
            statsMap['Defense'] = value;
            break;
          case 'special-attack':
            statsMap['Sp.Atk'] = value;
            break;
          case 'special-defense':
            statsMap['Sp.Def'] = value;
            break;
          case 'speed':
            statsMap['Speed'] = value;
            break;
        }
      }

      // Compute total of all six base stats
      statsMap['Total'] =
        statsMap['HP'] +
        statsMap['Attack'] +
        statsMap['Defense'] +
        statsMap['Sp.Atk'] +
        statsMap['Sp.Def'] +
        statsMap['Speed'];

      return statsMap;
    });
  }

  function drawPlotly3D() {
    const statKeys = ['Total', 'HP', 'Attack', 'Defense', 'Sp.Atk', 'Sp.Def', 'Speed'];

    const validRows = statData.filter((d) =>
      statKeys.every((k) => d[k] !== undefined && d[k] !== '' && !isNaN(+d[k])),
    );

    const matrix = validRows.map((d) => statKeys.map((k) => +d[k]));
    const pca = new PCA(matrix);
    const scoresMatrix = pca.predict(matrix);
    const scores = scoresMatrix.to2DArray();
    const explained = pca.getExplainedVariance(); // returns [%, %, %, ...]
    const cumulative = explained.slice(0, 3).reduce((a, b) => a + b, 0);

    const points = validRows.map((d, i) => ({
      Name: d.Name,
      Variant: d.Variant,
      PC1: scores[i][0],
      PC2: scores[i][1],
      PC3: scores[i][2],
    }));

    const trace = {
      x: points.map((d) => d.PC1),
      y: points.map((d) => d.PC2),
      z: points.map((d) => d.PC3),
      text: points.map((d) =>
        d.Variant && d.Variant.trim() !== '' ? `${d.Variant} ${d.Name}` : d.Name,
      ),
      mode: 'markers',
      type: 'scatter3d',
      marker: {
        size: 4,
        color: points.map((d) => d.PC1),
        colorscale: 'Viridis',
        opacity: 0.8,
      },
    };

    const layout = {
      margin: { l: 0, r: 0, b: 0, t: 0 },
      scene: {
        xaxis: { title: 'PC1' },
        yaxis: { title: 'PC2' },
        zaxis: { title: 'PC3' },
      },
    };

    Plotly.newPlot('chart3d', [trace], layout);
  }

  function updateChartFromQueried() {
    statData = getQueriedPokemonStats();
    if (Plotly) {
      drawPlotly3D();
    }
  }

  $effect(() => {
    if (Object.keys(queried_pokemon).length > 0) {
      updateChartFromQueried();
    }
  });

  let Plotly = $state(null);

  onMount(async () => {
    statData = getQueriedPokemonStats();
    Plotly = (await import('plotly.js-dist-min')).default;
    console.log(Plotly);
  });
</script>

<!-- Chart 3: PCA -->
<div class="flex h-full flex-col">
  <h3 style="margin-left: 1rem;">
    7 pokemon statistics reduced to 3 dimensions representing 94% of variance
  </h3>
  <div id="chart3d" class="h-full"></div>
</div>

<style>
  #chart3d {
    margin: 2rem 1rem;
  }

  :global(body) {
    margin-bottom: 4rem;
  }
</style>
