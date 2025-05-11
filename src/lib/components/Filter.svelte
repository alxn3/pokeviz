<script lang="ts">
  export type FilterOptions = {
    [key: string]: {
      name: string;
      value: string;
      class?: string;
    }[];
  };

  export type FilterValues = {
    [key: string]: string[];
  };

  let {
    filterOptions,
    values = $bindable(),
  }: {
    filterOptions: FilterOptions;
    values: FilterValues;
  } = $props();
</script>

<div class="space-y-4">
  <div class="flex items-end justify-between">
    <h1 class="text-2xl font-light">Filter</h1>
    <div class="space-x-2">
      <button
        class="text-base-600 hover:text-base-800 cursor-pointer"
        onclick={() => {
          for (const key in values) {
            values[key] = filterOptions[key].map(
              (item) => item.value,
            );
          }
        }}
      >
        All
      </button>
      <button
        class="text-base-600 hover:text-base-800 cursor-pointer"
        onclick={() => {
          for (const key in values) {
            values[key] = [];
          }
        }}
      >
        None
      </button>
    </div>
  </div>
  {#each Object.entries(filterOptions) as [key, value]}
    <div class="space-y-1">
      <div class="flex items-center justify-between">
        <h1 class="text-xl font-light">{key.toUpperCase()}</h1>
        <div class="font-semibold">
          <button
            class="text-base-600 hover:text-base-800 cursor-pointer"
            onclick={() => {
              values[key] = filterOptions[key].map(
                (item) => item.value,
              );
            }}
          >
            +
          </button>
          <button
            class="text-base-600 hover:text-base-800 cursor-pointer"
            onclick={() => {
              values[key] = [];
            }}
          >
            -
          </button>
        </div>
      </div>
      <div class="text-base-800 flex flex-wrap gap-1">
        {#each value as item}
          <div class="flex text-center select-none">
            <input
              class="peer hidden"
              type="checkbox"
              id={item.value}
              name={item.name}
              value={item.value}
              bind:group={values[key]}
            />
            <label
              class={`text-base-600 border-base-600 peer-checked:text-base-50 h-7 min-w-7 rounded-lg border-1 px-2 py-0.5 ${item.class || 'peer-checked:bg-base-800 peer-checked:border-base-900'}`}
              for={item.value}>{item.name}</label
            >
          </div>
        {/each}
      </div>
    </div>
  {/each}
</div>
