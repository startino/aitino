<script lang="ts">
	import { writable } from 'svelte/store';

	import { Shell } from '$lib/components/layout/shell';
	import { SideNav } from '$lib/components/ui/side-nav';

	import { CircleUserRound, Dna, LogOut, MessagesSquare, UsersRound, Zap } from 'lucide-svelte';
	import type { ComponentType } from 'svelte';
	import { UserCheck, type Icon } from 'lucide-svelte';
	import { LocalAuth } from '$lib/components/ui/local-auth';

	export let data;

	let navigations: {
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
					name: 'Home',
					href: '/app/home',
					icon: Zap,
					current: false
				},
				{
					name: 'Projects',
					href: '/app/projects',
					icon: MessagesSquare,
					current: false
				}
			]
		}
	];
	let bottomNavigation = [{ name: 'Logout', href: 'logout', icon: LogOut, current: false }];
</script>

<LocalAuth>
	<Shell
		class="h-screen w-full max-w-none"
		slotSidebarLeft="m-4"
		slotPageContent="m-4"
		slotPageHeader="my-4"
	>
		<svelte:fragment slot="sidebarLeft"></svelte:fragment>

		<slot />
	</Shell>
</LocalAuth>
