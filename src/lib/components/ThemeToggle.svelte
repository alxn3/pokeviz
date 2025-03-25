<script lang="ts">
  import { Sun, SunMoon } from '@lucide/svelte';

  let isDark = $state(false);

  const toggle = () => {
    document.documentElement.classList.toggle('dark');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    localStorage.setItem(
      'theme',
      document.documentElement.classList.contains('dark')
        ? prefersDark
          ? 'system'
          : 'dark'
        : prefersDark
          ? 'light'
          : 'system',
    );

    isDark = document.documentElement.classList.contains('dark');
  };

  $effect(() => {
    isDark = document.documentElement.classList.contains('dark');
  });
</script>

<button
  class="hover:text-accent-400 cursor-pointer font-black transition-colors"
  onclick={toggle}
  aria-label="theme toggle"
>
  {#if isDark}
    <SunMoon />
  {:else}
    <Sun />
  {/if}
</button>
