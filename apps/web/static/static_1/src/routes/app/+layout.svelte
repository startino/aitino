<script lang="ts">
	import { SvelteFlowProvider } from "@xyflow/svelte";
	import { Menu } from "lucide-svelte";
	import { writable } from "svelte/store";

	import { Button } from "$lib/components/ui/button";
	import * as Sheet from "$lib/components/ui/sheet";
	import { setContext } from "$lib/utils";

	let menuOpen = false;
	let navGroups = [
		{
			name: null,
			baseSrc: "/app",
			items: [
				{
					label: "Sessions",
					src: "/sessions"
				}
			]
		},
		{
			name: "Editors",
			baseSrc: "/app/editors",
			items: [
				{
					label: "Crew",
					src: "/crew"
				},
				{
					label: "Agent",
					src: "/agent"
				}
			]
		},
		{
			name: null,
			baseSrc: "",
			items: [
				{
					label: "Account",
					src: "/app/account"
				},
				{
					label: "Help",
					src: "https://discord.gg/sAzxPpr9a8"
				}
			]
		}
	];

	setContext("crew", {
		receiver: writable(null),
		count: writable({ agents: 0, prompts: 0 })
	});
</script>

<Sheet.Root open={menuOpen} onOpenChange={(open) => (menuOpen = open)}>
	<Sheet.Trigger asChild let:builder>
		<Button builders={[builder]} class="fixed left-6 top-6 z-10 ml-auto block">
			<Menu />
		</Button>
	</Sheet.Trigger>

	<Sheet.Content side="left">
		<nav class="grid justify-center gap-6 text-center">
			{#each navGroups as group}
				<div>
					{#if group.name}
						<h2 class="text-sm font-bold uppercase leading-relaxed text-accent-400">
							{group.name}
						</h2>
					{/if}
					<ul class="grid gap-1">
						{#each group.items as item}
							<li>
								<a href="{group.baseSrc}{item.src}" on:click={() => (menuOpen = false)}>
									{item.label}
								</a>
							</li>
						{/each}
					</ul>
				</div>
			{/each}
		</nav>
	</Sheet.Content>
</Sheet.Root>

<main>
	<SvelteFlowProvider>
		<slot />
	</SvelteFlowProvider>
</main>
