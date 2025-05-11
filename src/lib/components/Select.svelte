<script lang="ts">
  let {
    options,
    value = $bindable(),
    ...props
  }: {
    options: {
      name: string;
      value: string;
    }[];
    value: string;
    name?: string;
    index?: string;
    class?: string;
  } = $props();
</script>

<div class={`flex flex-wrap gap-2 ${props.class}`}>
  {#each options as option}
    <div class="flex select-none">
      <input
        type="radio"
        name={'select_' + props.index}
        class="peer hidden"
        id={option.value + props.index}
        bind:group={value}
        value={option.value}
      />
      <label
        for={option.value + props.index}
        class="border-base-300 bg-base-100 text-base-600 peer-checked:border-base-900 peer-checked:bg-base-900 peer-checked:text-base-50 cursor-pointer rounded-lg border-2 px-2 py-0.5"
      >
        {option.name}
      </label>
    </div>
  {/each}
</div>
