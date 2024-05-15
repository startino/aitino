<script lang="ts">
	import { page } from '$app/stores';
	import {
		Paperclip,
		Receipt,
		PencilRuler,
		PlusCircle,
		PieChart,
		Building,
		Table,
		ScrollText
	} from 'lucide-svelte';
	import type { SvelteComponent } from 'svelte';
</script>

<!-- Static sidebar for desktop -->
<div class="hidden h-full overflow-y-clip lg:z-50 lg:flex lg:w-72 lg:flex-col">
	<!-- Sidebar component, swap this element with another sidebar if you like -->
	<div
		class="m-4 flex grow flex-col gap-y-5 overflow-hidden rounded-2xl border bg-primary-900/20 px-6 pb-6 text-white"
	>
		<div class="flex h-16 shrink-0 items-center px-2 pt-6">
			<a href="https://flowbite.com" class="mr-4 flex place-items-center space-x-2">
				<Logo color="accent" />
				<span class="self-center whitespace-nowrap text-2xl font-semibold dark:text-white">Oak</span
				>
			</a>
		</div>
		<nav class="flex flex-col pt-0 sm:mt-0 sm:pt-0">
			<ul role="list" class="flex list-none flex-col gap-y-0 pl-0 sm:mt-0 sm:pl-0">
				<li class="my-0 pl-0 sm:my-0 sm:pl-0">
					{#each navigations as { name, items }}
						<ul role="list" class=" mb-6 list-none gap-4 pl-0 sm:mb-8 sm:pl-0">
							<p class="m-0 px-2 pb-2 text-xs font-semibold sm:m-0">{name}</p>
							{#each items as { name, href, icon, current, pendingCount }}
								<li class="m-0 pl-0 sm:m-0 sm:pl-0">
									<!-- Current: "bg-gray-800 text-primary-foreground", Default: "text-gray-400 hover:text-primary-foreground hover:bg-gray-800" -->
									<a
										href={'/home/' + href}
										class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold transition transition-colors transition-transform hover:translate-x-2 hover:scale-[1.04] {$page.url.pathname.includes(
											href
										)
											? 'bg-accent/90 text-accent-foreground hover:bg-accent '
											: 'text-primary-foreground opacity-100 hover:text-accent'}"
									>
										<LucideIcon name={icon} />
										{name}
										{#if pendingCount}
											<span
												class="ml-auto rounded-full bg-accent px-2 py-1 text-xs font-semibold text-accent-foreground"
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
									href={'/home/' + href}
									class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold transition transition-colors transition-transform hover:translate-x-2 hover:scale-[1.04] {$page.url.pathname.includes(
										href
									)
										? 'bg-accent/90 text-accent-foreground hover:bg-accent '
										: 'text-primary-foreground opacity-100 hover:text-accent'}"
								>
									<LucideIcon name={icon} />
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
