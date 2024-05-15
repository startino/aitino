<script lang="ts">
	import { base } from '$app/paths';
	import Logo from '$lib/components/atoms/Logo.svelte';
</script>

<footer
	class="{$$props.class} pt-20 p-6 border-t  border-secondary/10">
	<div
		class="sm:flex sm:justify-between sm:items-center md:px-10 lg:px-20 xl:px-40 px-auto md:px-auto">
		<Logo />
		<ul
			class="flex flex-wrap items-center mb-6 space-x-6 text-sm sm:mb-0  text-background-on">
			<li>
				<a
					class="inline  text-secondary hover:text-tertiary"
					href={base}>
					Privacy Policy
				</a>
			</li>
			<li>
				<a
					class="inline  text-secondary hover:text-tertiary"
					href={base}>
					Licensing
				</a>
			</li>
			<li>
				<a
					class="inline  text-secondary hover:text-tertiary"
					href={base}>
					Pricing
				</a>
			</li>
		</ul>
	</div>
	<hr class="my-6 sm:mx-auto lg:my-8  border-secondary/10" />
	<span class="block text-sm sm:text-center  text-background-on">
		Unpublished © 2023
		<a
			href="{base}/"
			class=" text-tertiary hover:underline hover:">
			Futino™
		</a>
	</span>
</footer>
