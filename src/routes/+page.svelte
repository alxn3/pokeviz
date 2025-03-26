<script lang="ts">
  const type_colors = [
    'type-normal',
    'type-fighting',
    'type-flying',
    'type-poison',
    'type-ground',
    'type-rock',
    'type-bug',
    'type-ghost',
    'type-steel',
    'type-fire',
    'type-water',
    'type-grass',
    'type-electric',
    'type-psychic',
    'type-ice',
    'type-dragon',
    'type-dark',
    'type-fairy',
    'type-stellar',
  ];
</script>

<div
  class="bg-base-50 border-base-300 mx-auto flex w-fit max-w-full flex-col gap-6 rounded-xl border p-4"
>
  <div>
    <p class="text-base-700 text-xl font-light tracking-widest uppercase">base</p>
    <div class="flex gap-2">
      <div class="border-base-300 bg-base-50 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-100 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-200 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-300 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-400 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-500 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-600 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-700 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-800 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-900 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-base-950 h-16 w-16 rounded-xl border"></div>
    </div>
  </div>
  <div>
    <p class="text-base-700 text-xl font-light tracking-widest uppercase">accent</p>
    <div class="flex gap-2">
      <div class="border-base-300 bg-accent-50 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-100 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-200 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-300 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-400 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-500 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-600 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-700 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-800 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-900 h-16 w-16 rounded-xl border"></div>
      <div class="border-base-300 bg-accent-950 h-16 w-16 rounded-xl border"></div>
    </div>
  </div>
  <div class="grid grid-cols-[repeat(auto-fit,minmax(20em,1fr))] gap-x-4 gap-y-2">
    {#each type_colors as type}
      <div>
        <p class="text-base-700 text-lg font-light tracking-widest uppercase">{type.slice(5)}</p>
        <div class="*:border-base-500/30 flex gap-1 *:h-8 *:grow *:rounded-lg *:border">
          <div class="{type} bg-type-50"></div>
          <div class="{type} bg-type-100"></div>
          <div class="{type} bg-type-200"></div>
          <div class="{type} bg-type-300"></div>
          <div class="{type} bg-type-400"></div>
          <div class="{type} bg-type-500"></div>
          <div class="{type} bg-type-600"></div>
          <div class="{type} bg-type-700"></div>
          <div class="{type} bg-type-800"></div>
          <div class="{type} bg-type-900"></div>
          <div class="{type} bg-type-950"></div>
        </div>
      </div>
    {/each}
  </div>
</div>
