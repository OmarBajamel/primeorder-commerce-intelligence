.PHONY: bootstrap demo test screenshots release-check clean

bootstrap:
	pnpm bootstrap

demo:
	pnpm data:generate
	pnpm dev:web

test:
	pnpm test

screenshots:
	pnpm screenshots

release-check:
	pnpm release:check

clean:
	pnpm clean
