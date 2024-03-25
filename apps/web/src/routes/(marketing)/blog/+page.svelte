<script lang="ts">
	import SEO from '$lib/components/SEO/index.svelte';
</script>

<SEO
	slug="blog"
	title="Blog • Aitino"
	metadescription="This is a collection of blogs written by Aitino to raise awareness of the capabilities of multi-agent systems, especially in this modern age of powerful AI models."
/>

<div class="mt-32 min-h-96 md:mt-64">
	<div class="mx-auto max-w-7xl px-6 lg:px-8">
		<div class="mx-auto max-w-2xl overflow-hidden lg:max-w-4xl">
			<h2
				class="bg-gradient-to-b from-foreground to-primary bg-clip-text text-center text-3xl font-bold tracking-tight text-transparent sm:text-4xl"
			>
				Blog
			</h2>
			<p class="mt-2 text-center text-lg leading-8 text-foreground/80"></p>
			<div
				class="mx-auto mt-16 space-y-20 text-center font-bold text-primary lg:mt-20 lg:space-y-20"
			>
				COMING SOON!
				<!-- {#each data.posts as post}
					{#if post.published}
						<a href="/blog/{post.slug}" class="group">
							<article
								class="relative isolate flex flex-col gap-8 lg:grid lg:grid-cols-4"
								data-pubdate={post.date}
							>
								<div
									class="col-span-1 lg:aspect-1 relative aspect-[16:9] sm:aspect-[2/1] lg:h-full lg:shrink-0"
								>
									<img
										src={post.thumbnail}
										alt="Thumbnail for {post.title}"
										class="absolute inset-0 h-full w-full rounded-2xl bg-card object-cover"
									/>
									<div
										class="absolute inset-0 rounded-2xl ring-1 ring-inset ring-background/10"
									></div>
								</div>
								<div class="col-span-3">
									<div class="flex items-center gap-x-4 text-xs">
										<time datetime={post.date} class="text-foreground/70">{post.date_formatted}</time>
										<a
											href="#"
											class="hover:bg- relative z-10 rounded-full bg-primary px-3 py-1.5 font-medium text-primary-foreground"
											>{post.category}</a
										>
									</div>
									<div class="group relative max-w-xl">
										<h3
											class="mt-2 text-lg font-semibold leading-6 text-foreground group-hover:text-foreground/80"
										>
											{post.title}
										</h3>
										<p class="mt-3 text-xs leading-6 text-foreground/80">
											{post.description}
										</p>
									</div>
									<div class="mt-2 flex border-t border-gray-900/5 pt-2">
										<div class="relative flex items-center gap-x-4">
											<img
												src="{post.author == "Jorge Lewis" ? "/people/jorge-lewis.png" : (post.author == "Jonas Lindberg" ? "/people/jonas-lindberg.jpg" : "/favicon.png")}"
												alt="{post.author}'s Profile Picture"
												class="h-10 w-10 rounded-full bg-card"
											/>
											<div class="text-sm leading-6">
												<p class="font-semibold text-foreground">{post.author}</p>
											</div>
										</div>
									</div>
								</div>
							</article>
						</a>
					{/if}
				{/each} -->
			</div>
		</div>
	</div>
</div>
