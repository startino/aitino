<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
	import FormItem from './FormItem.svelte';
</script>

<div class="relative mx-auto flex w-full flex-col gap-y-12 text-white lg:gap-y-4">
	<h1 class="prose-sm text-balance text-center">
		Join the Future of AI<br /> with Exclusive Early Access to
		<span class="inline-block border-none text-primary">Aitino</span>
	</h1>

	<p class="mx-auto mt-2 max-w-3xl text-center text-lg">
		<span class="text-primary">Aitino </span> is a SaaS platform powered by multi-agent LLMs designed
		to help entrepreneurs and businesses automate tasks and solve complex problems.
	</p>

	<FormItem class="mt-10" />
</div>
