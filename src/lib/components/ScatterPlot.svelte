<!-- Reference Code from https://plotly.com/javascript/3d-scatter-plots/ -->
<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import { PCA } from 'ml-pca';

  const statOptions = ["Total", "HP", "Attack", "Defense", "Sp.Atk", "Sp.Def", "Speed"];
  let selectedX1 = "Speed";   // Chart 1: stat vs Popularity
  let selectedX = "Attack";   // Chart 2: stat vs stat
  let selectedY = "Speed";

  const margin = { top: 40, right: 30, bottom: 50, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

  let popularityData = [];
  let statData = [];

  /**
   * @param {string} containerId
   * @param {any[]} dataset
   * @param {string} xKey
   * @param {string} yKey
   * @param {string} xLabel
   * @param {string} yLabel
   * @param {string} title
   */
  function drawScatterplot(containerId, dataset, xKey, yKey, xLabel, yLabel, title) {
    const svg = d3.select(containerId)
        .html("")
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Tooltip div (reused across charts)
    const tooltip = d3.select("#tooltip");

    dataset.forEach(d => {
        d[xKey] = +d[xKey];
        d[yKey] = +d[yKey];
    });

    const x = d3.scaleLinear()
        .domain([0, d3.max(dataset, d => d[xKey])])
        .range([0, width]);

    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    const y = d3.scaleLinear()
        .domain([0, d3.max(dataset, d => d[yKey])])
        .range([height, 0]);

    svg.append("g")
        .call(d3.axisLeft(y));

    svg.append("text")
        .attr("text-anchor", "end")
        .attr("x", width / 2)
        .attr("y", height + 40)
        .text(xLabel);

    svg.append("text")
        .attr("text-anchor", "end")
        .attr("transform", "rotate(-90)")
        .attr("y", -50)
        .attr("x", -height / 2)
        .text(yLabel);

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", -20)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-weight", "bold")
        .text(title);

    svg.append('g')
        .selectAll("circle")
        .data(dataset)
        .enter()
        .append("circle")
        .attr("cx", d => x(d[xKey]))
        .attr("cy", d => y(d[yKey]))
        .attr("r", 3)
        .style("fill", "#69b3a2")
        .on("mouseover", (event, d) => {
            const variantPrefix = d.Variant && d.Variant.trim() !== "" ? `${d.Variant} ` : "";
            tooltip
                .style("opacity", 1)
                .html(`<strong>${variantPrefix}${d.Name}</strong>`)
                .style("left", event.pageX + 10 + "px")
                .style("top", event.pageY - 28 + "px");
            })
        .on("mousemove", event => {
            tooltip
            .style("left", event.pageX + 10 + "px")
            .style("top", event.pageY - 28 + "px");
        })
        .on("mouseout", () => {
            tooltip.style("opacity", 0);
        });
  }

  
  function updateChart1() {
    const popularityMap = new Map(popularityData.map(d => [d.Name, +d.Popularity]));
    const merged = statData
      .filter(d => popularityMap.has(d.Name))
      .map(d => ({
        ...d,
        [selectedX1]: +d[selectedX1],
        Popularity: popularityMap.get(d.Name)
      }));
    drawScatterplot("#chart1", merged, selectedX1, "Popularity", selectedX1, "Popularity", `${selectedX1} vs Popularity`);
  }

  function updateChart2() {
    drawScatterplot("#chart2", statData, selectedX, selectedY, selectedX, selectedY, `${selectedX} vs ${selectedY}`);
  }

  function drawPlotly3D(data) {
    const statKeys = ["Total", "HP", "Attack", "Defense", "Sp.Atk", "Sp.Def", "Speed"];

    const validRows = data.filter(d =>
      statKeys.every(k => d[k] !== undefined && d[k] !== "" && !isNaN(+d[k]))
    );

    const matrix = validRows.map(d => statKeys.map(k => +d[k]));
    const pca = new PCA(matrix);
    const scoresMatrix = pca.predict(matrix);
    const scores = scoresMatrix.to2DArray();
    const explained = pca.getExplainedVariance(); // returns [%, %, %, ...]
    const cumulative = explained.slice(0, 3).reduce((a, b) => a + b, 0);
    console.log(`First 3 PCs explain about ${Math.round(cumulative * 100)}% of variance`);

    const points = validRows.map((d, i) => ({
      Name: d.Name,
      Variant: d.Variant,
      PC1: scores[i][0],
      PC2: scores[i][1],
      PC3: scores[i][2]
    }));

    const trace = {
      x: points.map(d => d.PC1),
      y: points.map(d => d.PC2),
      z: points.map(d => d.PC3),
      text: points.map(d =>
        d.Variant && d.Variant.trim() !== ""
          ? `${d.Variant} ${d.Name}`
          : d.Name
      ),
      mode: 'markers',
      type: 'scatter3d',
      marker: {
        size: 4,
        color: points.map(d => d.PC1),
        colorscale: 'Viridis',
        opacity: 0.8
      }
    };

    const layout = {
      margin: { l: 0, r: 0, b: 0, t: 0 },
      scene: {
        xaxis: { title: 'PC1' },
        yaxis: { title: 'PC2' },
        zaxis: { title: 'PC3' }
      }
    };

    Plotly.newPlot('chart3d', [trace], layout);
  }

  onMount(() => {
    Promise.all([
      d3.csv('/pokedex_full.csv'),
      d3.csv('/popularity.csv')
    ]).then(([pokedex, popularity]) => {
      statData = pokedex;
      popularityData = popularity;
      updateChart1();
      updateChart2();
      loadPlotly3D(pokedex);
    });
  });

  /* need to use document to */
  function loadPlotly3D(data) {
    const script = document.createElement("script");
    script.src="https://cdn.plot.ly/plotly-2.27.0.min.js";
    script.onload = () => drawPlotly3D(data);
    document.body.appendChild(script);
  }

</script>

<!-- Chart 1: Stat vs Popularity -->
<div id="chart1"></div>

<h3 style="margin-left:1rem;">Chart 1: Select X-axis:</h3>
<div class="button-group">
  {#each statOptions as option}
    <button
      class:selected={selectedX1 === option}
      on:click={() => {
        selectedX1 = option;
        updateChart1();
      }}>
      {option}
    </button>
  {/each}
</div>

<!-- Chart 2: Stat vs Stat -->
<div id="chart2"></div>

<h3 style="margin-left:1rem;">Chart 2: Select X-axis:</h3>
<div class="button-group">
  {#each statOptions as option}
    <button
      class:selected={selectedX === option}
      on:click={() => {
        selectedX = option;
        updateChart2();
      }}>
      {option}
    </button>
  {/each}
</div>

<h3 style="margin-left:1rem; margin-top: 1.5rem;">Chart 2: Select Y-axis:</h3>
<div class="button-group">
  {#each statOptions as option}
    <button
      class:selected={selectedY === option}
      on:click={() => {
        selectedY = option;
        updateChart2();
      }}>
      {option}
    </button>
  {/each}
</div>
<div id="tooltip" class="tooltip" style="opacity: 0;"></div>


<!-- Chart 3: Stat vs Stat -->
<h3 style="margin-left: 1rem;">PCA Plot</h3>
<h3 style="margin-left: 1rem;">7 pokemon statistics reduced to 3 dimensions representing 94% of variance</h3>
<div id="chart3d" style="height: 500px;"></div>

<style>
  #chart1, #chart2, #chart3d {
    margin: 2rem 1rem;
  }

  :global(body) {
    margin-bottom: 4rem;
  }

  .button-group {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0 1rem 1rem 1rem;
  }

  button {
    padding: 0.4rem 0.8rem;
    font-size: 0.95rem;
    cursor: pointer;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: white;
  }

  button.selected {
    background-color: #69b3a2;
    color: white;
    border-color: #69b3a2;
    font-weight: bold;
  }


    .tooltip {
    position: absolute;
    text-align: center;
    padding: 6px 10px;
    font-size: 0.85rem;
    background: #333;
    color: #fff;
    border-radius: 4px;
    pointer-events: none;
    transition: opacity 0.2s ease;
    z-index: 10;
    }

</style>
