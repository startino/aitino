<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { AppShell } from '$lib/components/layout/shell';
	import * as Tabs from '$lib/components/ui/tabs';

	const baseHref = '/app/account';
	const navItems = [
		{ href: `${baseHref}`, label: 'Profile' },
		{ href: `${baseHref}/subscription`, label: 'Subscription' },
		{ href: `${baseHref}/api-keys`, label: 'Your API Keys' }
	];
</script>

<AppShell>
	<Tabs.Root value={$page.url.pathname}>
		<Tabs.List class="grid w-full grid-cols-3">
			{#each navItems as { href, label }}
				<Tabs.Trigger on:click={() => goto(href)} value={href}>{label}</Tabs.Trigger>
			{/each}
		</Tabs.List>
		<slot />
	</Tabs.Root>
</AppShell>
