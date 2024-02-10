import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import { type ViteDevServer } from 'vite';

import { Server } from 'socket.io';

const webSocketServer = {
	name: 'webSocketServer',
	configureServer(server: ViteDevServer) {
		if (!server.httpServer) return;

		const io = new Server(server.httpServer);

		io.on('connection', (socket) => {
			socket.emit('eventFromServer', 'Hello, World 👋');
		});
		io.on('message', async (message: string) => {
			console.log(message);
			await new Promise((r) => setTimeout(r, 2000));
			io.emit("eventFromServer", "hello to you to!");
		});
	}
};
export default defineConfig({
	plugins: [sveltekit(), webSocketServer],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
