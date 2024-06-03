<script lang="ts">
	import '$styling';
</script>

<main
	class="bg-background text-background-on relative min-h-screen w-full overflow-hidden text-center"
>
	<!-- The content -->
	<arcitle class="relative flex min-h-screen w-full flex-col items-center justify-center gap-24">
		<slot />
	</arcitle>
</main>
