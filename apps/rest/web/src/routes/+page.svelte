Hey
<script lang="ts">
	// This was added for the purpose of rebuilding the project lol. its not deploying.
	// if this is still here you can proibably delete it
	import { Button } from '$lib/components/ui/button';


</script>

<!-- Hero -->
<section
	id="hero"
	class="md:prose-md prose prose-sm prose-main flex h-screen w-full max-w-7xl flex-col items-center justify-center gap-2 px-5 text-lg sm:prose-base lg:prose-lg xl:prose-xl sm:px-10 sm:text-xl md:text-2xl lg:text-4xl"
>
	<div
		class="z-100 pointer-events-none absolute left-0 right-0 top-0 h-screen border-b border-primary/40 shadow-2xl"
	></div>
	<div class="flex flex-col">
		<h1 class="m-0 sm:m-0">
			Building <br /><span
				class="m-0 bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:m-0"
			>
				Ideas
			</span>
			Into
            <a href="#pricing" class="bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:m-0">
                Reality
			<span
				class="m-0 bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:m-0"
			>
				Life
			</span>

			<br />
		</h1>
	</div>
	<p class="text-pretty opacity-80">
		Advancing the success of non-technical entrepreneurs and startups by providing the passion and
		commitment of a tech co-founder alongside the efficiency and reliability of a professional
		development agency.
	</p>

	<div class="not-prose flex gap-4">
		<Button href="#pricing"  class="px-12 py-7 text-2xl"
			>Get in Touch</Button
		>
		<Button href="#pricing" class="px-12 py-7 text-2xl" variant="outline">Pricing</Button>
	</div>
</section>

<!-- Solution -->
<section
	class="md:prose-md prose prose-sm prose-main flex max-w-7xl flex-col items-center justify-center px-5 sm:prose-base lg:prose-lg xl:prose-xl 2xl:prose-2xl sm:px-10"
>
	<h2
		class="mt-0 bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:mt-0"
	>
		Our Offer
	</h2>
	<p>
		Benefit from a partnership that offers the
		<b class="underline decoration-secondary decoration-2 underline-offset-4">
			long-term dedication
		</b>
		and
		<b class="underline decoration-primary decoration-2 underline-offset-4">
			passion of a co-founder,
		</b>
		enhanced by the
		<b class="underline decoration-secondary decoration-2 underline-offset-4">
			professional execution
		</b>
		of a seasoned development agency. By taking a piece of the pie through equity or revenue share, we
		ensure our
		<b class="underline decoration-primary decoration-2 underline-offset-4">
			goals align with yours.
		</b>
		We’ll be at your side to provide
		<b class="underline decoration-secondary decoration-2 underline-offset-4">strategic insights</b>
		and
		<b class="underline decoration-primary decoration-2 underline-offset-4">ongoing support</b> to ensure
		your product not only reaches the market but thrives.
	</p>
</section>

<!-- Our Specialties -->
<!-- TODO: Improve this section by adding descriptions to the specialties -->
<section
	class="md:prose-md prose prose-sm prose-main flex max-w-7xl flex-col items-center justify-center px-5 sm:prose-base lg:prose-lg xl:prose-xl 2xl:prose-2xl sm:px-10"
>
	<h2
		class=" mt-0 bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:mt-0"
	>
		Our Specialties
	</h2>

</section>

<!-- Process Section -->
<section
	class="md:prose-md prose prose-sm prose-main flex max-w-7xl flex-col items-center justify-center px-5 sm:prose-base lg:prose-lg xl:prose-xl 2xl:prose-2xl sm:px-10"
>
	<div class="inner-section flex flex-col md:gap-12">
		<div class="mx-auto w-fit max-w-xl">
			<h2
				class="mt-0 bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:mt-0"
			>
				How We Roll
			</h2>
			<p>The lifecycle of our partnership in three easy steps.</p>
		</div>
		<div class="grid grid-cols-1 place-items-center gap-y-6 md:grid-cols-3">
			{#each process as { title, body }, i}
				<div class="relative flex h-full w-full">
					<!-- md+ Journey line and Chapter checkmark -->
					<div class="hidden md:flex">
						<div
							class="not-prose absolute top-0 hidden h-full w-full -translate-y-1/2 flex-row place-items-center text-center md:flex"
						>
							<!-- Circle -->
							<div
								class="z-10 flex h-11 w-11 items-center rounded-full bg-primary text-center text-primary-on"
							>
								<b class="z-20 mx-auto text-lg">{i + 1}</b>
							</div>

							<!-- Line -->
							<div class="my-2 -ml-6 flex h-1 w-2/3 rounded-full bg-primary" />
						</div>
						<div
							class="my-2 ml-12 mt-14 flex w-full flex-col py-4 pl-1 pr-8 text-left md:ml-0 md:mr-2"
						>
							<h3
								class="mt-0 bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:mt-0"
							>
								{title}
							</h3>
							<p class="title-medium md:headline-large max-w-xs">
								{body}
							</p>
						</div>
					</div>

					<!-- Mobile Journey line and Chapter checkmark -->
					<div class="flex flex-col md:hidden">
						<div
							class="not-prose absolute -top-2 left-4 flex h-full flex-col items-center text-center"
						>
							<!-- Circle -->
							<div
								class="z-10 flex h-12 w-11 items-center rounded-full bg-primary text-center text-primary-on"
							>
								<b class="z-20 mx-auto text-lg">
									{i + 1}
								</b>
							</div>

							<!-- Line -->
							<div class="mx-auto -mt-6 flex h-full w-1 rounded-full bg-primary" />
						</div>
						<div class="flex w-full flex-col pl-16 pr-4 pt-8 text-left">
							<h3
								class="mt-0 bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:mt-0"
							>
								{title}
							</h3>
							<p>
								{body}
							</p>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- About -->
<section id="about">
	<div class="mx-auto max-w-7xl px-6 lg:px-8">
		<div
			class="md:prose-md prose prose-sm prose-main mx-auto flex flex-col items-center justify-center px-5 sm:prose-base lg:prose-lg xl:prose-xl 2xl:prose-2xl sm:px-10"
		>
			<h2
				class="bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent"
			>
				<span class="relative text-primary/20">Y</span>our People
			</h2>
			<p class="mt-6 text-lg leading-8 opacity-80">
				At Startino, we're "people over process". We know a well rounded, experienced, and lean team
				produces better results. We’re a group of individuals who are passionate about what we do
				and dedicated to delivering the best results for our Co-Founders.
			</p>
		</div>
		<ul
			class="mx-auto mt-20 grid max-w-2xl grid-cols-1 gap-x-6 gap-y-20 text-left sm:grid-cols-2 lg:max-w-4xl lg:gap-x-8 xl:max-w-none"
		>
		</ul>
	</div>
</section>


<!-- Contact Section -->
<!-- About -->
<section >
	<div
id="contact"
		class="mx-auto grid max-w-7xl grid-cols-1 justify-items-center gap-8 px-6 md:grid-cols-2 lg:px-8"
	>
		<div class=" flex max-w-3xl flex-col gap-4 text-left">
			<h1 class="text-3xl font-bold tracking-tight text-background-on sm:text-4xl sm:text-6xl">
				Let's do this.
			</h1>
			<p class="text-base">
				We're excited to hear about your project. Fill out the form or reach out to us at <a
					class="text-accent underline"
					href="mailto:contact@futi.no">contact@futi.no</a
				> and we'll get back to you within 24 hours. Even better yet, let's have a virtual chat over
				coffee.
			</p>
			<Button
				href="https://cal.com/jorgelewis"
				variant="outline"
				target="new"
				class="group w-fit px-8 py-8 text-xl font-bold text-primary"
				>Book a Meeting!
			</Button>
		</div>
	</div>
</section>


<section class="mx-auto flex flex-col gap-8 px-6 pb-20 xl:px-16 2xl:px-64">
	<div
		class="md:prose-md prose prose-sm prose-main mx-auto flex flex-col items-center justify-center px-5 sm:prose-base lg:prose-lg xl:prose-xl 2xl:prose-2xl sm:px-10"
	>
		<h2
			class="mt-0 bg-gradient-to-b from-primary from-50% to-background bg-clip-text text-transparent sm:mt-0"
		>
			<span class="relative text-primary/20">Y</span>our Secret Sauce
		</h2>
		<p class="mt-6 text-pretty text-lg leading-8 opacity-80">
			The Robust and Agile Tech Stack Empowering Innovation, Efficiency, and Scalability.
		</p>
	</div>
	<ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-3">
		<li class="col-span-1 rounded-xl border border-primary shadow">
			<a
				href="https://svelte.dev/"
				target="_blank"
				class="flex items-center justify-between space-x-6 p-6"
			>
				<div class="flex-1">
					<div class="flex items-center space-x-3">
						<h3 class="text-nowrap text-sm font-medium text-background-on">Svelte & SvelteKit</h3>
						<span
							class="inline-flex flex-shrink-0 items-center rounded-full bg-secondary px-1.5 py-0.5 text-xs font-medium text-secondary-on ring-1 ring-inset ring-green-600/20"
							>Web Framework</span
						>
					</div>
					<p class="mt-1 w-full text-pretty text-left text-sm text-background-on/80">
						A web framework that shifts work out of the browser and into the build step, resulting
						in faster and more efficient apps.
					</p>
				</div>
				<img
					class="h-10"
					src="https://external-content.duckduckgo.com/ip3/svelte.dev.ico"
					alt="Svelte Logo"
				/>
			</a>
		</li>
		<li class="col-span-1 rounded-xl border border-primary shadow">
			<a
				href="https://www.typescriptlang.org/"
				target="_blank"
				class="flex items-center justify-between space-x-6 p-6"
			>
				<div class="flex-1">
					<div class="flex items-center space-x-3">
						<h3 class="text-sm font-medium text-background-on">TypeScript</h3>
						<span
							class="inline-flex flex-shrink-0 items-center rounded-full bg-secondary px-1.5 py-0.5 text-xs font-medium text-secondary-on ring-1 ring-inset ring-green-600/20"
							>Language</span
						>
					</div>
					<p class="mt-1 w-full text-pretty text-left text-sm text-background-on/80">
						TypeScript is a strongly typed programming language that builds on JavaScript, giving
						you better tooling at any scale.
					</p>
				</div>
				<img
					class="h-10"
					src="https://external-content.duckduckgo.com/ip3/www.typescriptlang.org.ico"
					alt="TypeScript Logo"
				/>
			</a>
		</li>
		<li class="col-span-1 rounded-xl border border-primary shadow">
			<a
				href="https://vercel.com"
				target="_blank"
				class="flex items-center justify-between space-x-6 p-6"
			>
				<div class="flex-1">
					<div class="flex items-center space-x-3">
						<h3 class="text-sm font-medium text-background-on">Vercel</h3>
						<span
							class="inline-flex flex-shrink-0 items-center rounded-full bg-secondary px-1.5 py-0.5 text-xs font-medium text-secondary-on ring-1 ring-inset ring-green-600/20"
							>Host</span
						>
					</div>
					<p class="mt-1 w-full text-pretty text-left text-sm text-background-on/80">
						Vercel is a platform that helps developers build, scale, and secure fast and
						personalized web products.
					</p>
				</div>
				<img
					class="h-10"
					src="https://external-content.duckduckgo.com/ip3/vercel.com.ico"
					alt="Vercel Logo"
				/>
			</a>
		</li>
		<li class="col-span-1 rounded-xl border border-primary shadow">
			<a
				href="https://www.cloudflare.com/"
				target="_blank"
				class="flex items-center justify-between space-x-6 p-6"
			>
				<div class="flex-1">
					<div class="flex items-center space-x-3">
						<h3 class="text-sm font-medium text-background-on">Cloudflare</h3>
						<span
							class="inline-flex flex-shrink-0 items-center rounded-full bg-secondary px-1.5 py-0.5 text-xs font-medium text-secondary-on ring-1 ring-inset ring-green-600/20"
							>Networking</span
						>
					</div>
					<p class="mt-1 w-full text-pretty text-left text-sm text-background-on/80">
						Cloudflare is a global cloud platform that provides network services to protect and
						optimize websites.
					</p>
				</div>
				<img
					class="h-10"
					src="https://external-content.duckduckgo.com/ip3/www.cloudflare.com.ico"
					alt="Cloudflare Logo"
				/>
			</a>
		</li>
		<li class="col-span-1 rounded-xl border border-primary shadow">
			<a
				href="https://fastapi.tiangolo.com/"
				target="_blank"
				class="flex items-center justify-between space-x-6 p-6"
			>
				<div class="flex-1">
					<div class="flex items-center space-x-3">
						<h3 class="text-sm font-medium text-background-on">FastAPI</h3>
						<span
							class="inline-flex flex-shrink-0 items-center rounded-full bg-secondary px-1.5 py-0.5 text-xs font-medium text-secondary-on ring-1 ring-inset ring-green-600/20"
							>API Framework</span
						>
					</div>
					<p class="mt-1 w-full text-pretty text-left text-sm text-background-on/80">
						FastAPI is a modern, fast (high-performance), web framework for building APIs with
						Python.
					</p>
				</div>
				<img
					class="h-10"
					src="https://external-content.duckduckgo.com/ip3/fastapi.tiangolo.com.ico"
					alt="FastAPI Logo"
				/>
			</a>
		</li>
		<li class="col-span-1 rounded-xl border border-primary shadow">
			<a
				href="https://www.python.org/"
				target="_blank"
				class="flex items-center justify-between space-x-6 p-6"
			>
				<div class="flex-1">
					<div class="flex items-center space-x-3">
						<h3 class="text-sm font-medium text-background-on">Python</h3>
						<span
							class="inline-flex flex-shrink-0 items-center rounded-full bg-secondary px-1.5 py-0.5 text-xs font-medium text-secondary-on ring-1 ring-inset ring-green-600/20"
							>Language</span
						>
					</div>
					<p class="mt-1 w-full text-pretty text-left text-sm text-background-on/80">
						Python is a versatile and powerful language that lets you work quickly and integrate
						systems more effectively.
					</p>
				</div>
				<img
					class="h-10"
					src="https://external-content.duckduckgo.com/ip3/www.python.org.ico"
					alt="Python Logo"
				/>
			</a>
		</li>
	</ul>
</section>


<section id="pricing">

heyy</section>
