<script lang="ts">
  import NavBar from '$lib/components/NavBar.svelte';
  import '../app.css';
  let { children } = $props();
</script>

<svelte:head>
  <script>
    const theme = localStorage.getItem('theme');

    document.documentElement.classList.add(
      !theme || theme === 'system'
        ? window.matchMedia('(prefers-color-scheme: dark)').matches
          ? 'dark'
          : 'light'
        : theme,
    );
  </script>
</svelte:head>

<header class="border-base-300 border-b">
  <div class="mx-auto w-[min(70rem,100%)]">
    <NavBar />
  </div>
</header>

<div class="mx-auto my-4 w-[min(70rem,100%)]">
  {@render children()}
</div>
