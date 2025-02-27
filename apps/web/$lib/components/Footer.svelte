<script lang="ts">
	// Your imports
	export let disabled = false;
</script>

<footer class="border-t py-6 md:py-0">
	<div class="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
		<p class="text-center text-sm leading-loose text-muted-foreground md:text-left">
			&copy; {new Date().getFullYear()} Aitino. All rights reserved.
		</p>
		<div class="flex gap-4">
			<span
				class="{disabled
					? 'cursor-not-allowed text-foreground/50'
					: 'text-muted-foreground underline underline-offset-4'} text-sm"
			>
				Terms
			</span>
			<span
				class="{disabled
					? 'cursor-not-allowed text-foreground/50'
					: 'text-muted-foreground underline underline-offset-4'} text-sm"
			>
				Privacy
			</span>
			<!-- Other footer links -->
		</div>
	</div>
</footer>
