<script lang="ts">
  import { getFallbackSprite } from '$lib/utils';
  import { Tooltip } from 'layerchart';
  import type { PokeData } from './PokeQuery.svelte';
  import type { Pokemon } from 'pokeapi-js-wrapper';
  import { type_colors } from '$lib/const';

  let {
    poke_data,
  }: {
    poke_data: PokeData;
  } = $props();

  const stat_to_name: { [key: string]: string } = {
    hp: 'HP',
    attack: 'Atk',
    defense: 'Def',
    'special-attack': 'Sp.Atk',
    'special-defense': 'Sp.Def',
    speed: 'Spe',
  };
</script>

<Tooltip.Root let:data class="overflow-clip rounded-xl border-1 p-0">
  <div class="bg-base-100 flex h-fit gap-2 p-1">
    <img
      class="bg-base-100 aspect-square h-full rounded-xl border"
      src={getFallbackSprite(data, poke_data)}
      alt={data.name}
    />
    <div class="flex flex-col">
      <div class="flex items-center justify-between gap-2">
        <p class="text-base-700 text-lg font-light tracking-widest uppercase">
          {data.name}
        </p>
        <div class="flex gap-1">
          {#each (data as Pokemon).types as { type }}
            <p
              class={`text-type-500 ${type_colors[type.name]} h-fit w-fit rounded-xl border px-2 py-0.5 text-xs font-medium tracking-widest`}
            >
              {type.name.slice(0, 3).toUpperCase()}
            </p>
          {/each}
        </div>
      </div>
      <slot {data} />
      <div class="flex w-72 flex-wrap items-start gap-0 space-y-1 space-x-1 pt-1">
        {#each (data as Pokemon).stats as { base_stat, stat }}
          <p
            class="text-base-600 w-fit rounded-xl border px-2 py-0.5 text-sm font-light tracking-widest"
          >
            {stat_to_name[stat.name]}: {base_stat}
          </p>
        {/each}
      </div>
    </div>
  </div>
</Tooltip.Root>
