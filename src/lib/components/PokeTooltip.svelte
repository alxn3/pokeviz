<script lang="ts">
  import { getFallbackSprite } from '$lib/utils';
  import { Tooltip } from 'layerchart';
  import type { PokeData } from './PokeQuery.svelte';

  let {
    poke_data,
  }: {
    poke_data: PokeData;
  } = $props();
</script>

<Tooltip.Root let:data class="overflow-clip rounded-xl border-1 p-0">
  <div class="bg-base-100 flex gap-2 p-1">
    <img
      class="bg-base-100 h-16 w-16 rounded-xl border"
      src={getFallbackSprite(data, poke_data)}
      alt={data.name}
    />
    <div class="flex flex-col">
      <p class="text-base-700 text-lg font-light tracking-widest uppercase">
        {data.name}
      </p>
      <p class="text-base-600 text-sm font-light tracking-widest">{data.name}</p>
    </div>
  </div>
</Tooltip.Root>
