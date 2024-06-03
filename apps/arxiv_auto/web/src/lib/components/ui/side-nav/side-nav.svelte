<script lang="ts">
	import { page } from '$app/stores';
	import { LogOut, Zap } from 'lucide-svelte';
	import type { ComponentType } from 'svelte';
	import type { Icon } from 'lucide-svelte';
	import { Logo } from '../logo';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';

	export let navigations: {
		name: string;
		items: {
			name: string;
			href: string;
			icon: ComponentType<Icon>;
			current: boolean;
			pendingCount?: number;
		}[];
	}[] = [
		{
			name: '',
			items: [
				{
					name: 'Auto-build',
					href: 'autobuild',
					icon: Zap,
					current: false
				}
			]
		}
	];
	export let bottomNavigation = [{ name: 'Logout', href: '/', icon: LogOut, current: false }]; // TODO: Make this button actually log out the user
</script>

<!-- Static sidebar for desktop -->
<div class=" flex h-full py-8 pl-4 lg:z-50 lg:w-72 lg:flex-col{$$props.class}">
	<!-- Sidebar component, swap this element with another sidebar if you like -->
	<div
		class="bg-primary-950/30 border-border flex grow flex-col gap-y-5 overflow-hidden rounded-2xl border px-6 pb-6 text-white"
	>
		<div class="flex h-16 shrink-0 items-center px-2 pt-6">
			<a href="/app/auto-build" class="mr-4 flex place-items-center space-x-2">
				<Logo />
				<span class="self-center whitespace-nowrap text-2xl font-semibold text-white"
					>Aitino <span class="text-sm">[v0.1.0]</span></span
				>
			</a>
		</div>
		<nav class="flex h-full flex-col sm:mt-0 sm:pt-0">
			<ul role="list" class="mb-5 flex h-full list-none flex-col gap-y-0 pl-0 pt-6 sm:mt-0 sm:pl-0">
				<li class="my-0 pl-0 sm:my-0 sm:pl-0">
					{#each navigations as { name, items }}
						<ul role="list" class=" mb-6 list-none gap-4 pl-0 sm:mb-8 sm:pl-0">
							<p class="text m-0 px-2 pb-2 text-xs font-semibold sm:m-0">{name}</p>
							{#each items as { name, href, icon, pendingCount }}
								<li class="m-0 pl-0 sm:m-0 sm:pl-0">
									<a
										{href}
										class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold transition transition-colors transition-transform hover:translate-x-2 hover:scale-[1.04] {$page.url.pathname.includes(
											href
										)
											? 'bg-accent/90 text-accent-foreground hover:bg-accent '
											: 'text-foreground hover:bg-primary/5 hover:text-accent opacity-100'}"
									>
										<svelte:component this={icon} />
										{name}
										{#if pendingCount}
											<span
												class="bg-accent text-accent-foreground ml-auto rounded-full px-2 py-1 text-xs font-semibold"
											>
												{pendingCount}
											</span>
										{/if}
									</a>
								</li>
							{/each}
						</ul>
					{/each}
				</li>
				<li class="mt-auto pl-0 sm:mt-auto sm:pl-0">
					<ul role="list" class=" m-0 list-none pl-0 sm:m-0 sm:pl-0">
						{#each bottomNavigation as { name, href, icon, current }}
							<li class="pb-0 pl-0 sm:pl-0">
								<a
									href={'/app/' + href}
									class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold transition transition-colors transition-transform hover:translate-x-2 hover:scale-[1.04] {$page.url.pathname.includes(
										href
									)
										? 'bg-accent/90 text-foreground hover:bg-accent '
										: 'text-foreground hover:bg-primary/5 hover:text-accent opacity-100'}"
								>
									<svelte:component this={icon} />
									{name}
								</a>
							</li>
						{/each}
					</ul>
				</li>
			</ul>
		</nav>
	</div>
</div>
