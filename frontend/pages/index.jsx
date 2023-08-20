import { useState, useCallback } from "react";
import Head from "next/head";
import axios from "axios";

const client = axios.create({
	baseURL: "http://127.0.0.1:8000/chat",
});

export default function Home() {
	const [currentChat, setCurrentChat] = useState();
	const [message, setMessage] = useState("");
	const [loading, setLoading] = useState(false);
	const [erorr, setError] = useState(false);

	const [chat, setChat] = useState([]);

	const submitForm = useCallback(
		e => {
			e.preventDefault();
			(async () => {
				setLoading(true);
				let response;
				try {
					if (currentChat) {
						response = await client.put(`/${currentChat}`, { message });
					} else {
						response = await client.post("/", { message });
						setCurrentChat(response.data.chat_id);
					}
					setChat([
						...chat,
						{
							id: Math.random() * 100,
							message: message,
							response: response.data.response,
						},
					]);
					setMessage("");
				} catch (e) {
					console.log(e);
				}
				setLoading(false);
			})();
		},
		[message, currentChat, chat]
	);

	const formatResponse = useCallback(response => {
		let text = "";
		response.split("\n").forEach(line => {
			line = line.replace(/!\[(.*)\]\((.*)\)/g, '<img src="$2" alt="$1" />');
			line = line.replace(/\[(.*)\]\((.*)\)/g, '<a href="$2" target="_blank">$1</a>');
			text += line + "<br />";
		});
		return text;
	}, []);

	return (
		<>
			<Head>
				<title>MyWardrobe</title>
			</Head>
			<main>
				<h1 className="text-center text-5xl font-bold shadow-lg italic text-yellow-300 py-6 bg-blue-600">
					mywardrobe.in
				</h1>
				<div className="py-6 px-12 flex flex-col gap-8">
					{chat.length > 0 ? (
						chat.map(c => (
							<div key={c.id} className="flex flex-col gap-8">
								<p className="self-end bg-blue-600 shadow-lg text-white p-4 rounded-xl font-medium">
									{c.message}
								</p>
								<p
									className="self-start bg-gray-200 shadow-lg text-gray-800 p-4 rounded-xl font-medium [&_img]:w-[200px] [&_a]:underline [&_a]:text-gray-600 hover:[&_a]:text-blue-500"
									dangerouslySetInnerHTML={{ __html: formatResponse(c.response) }}
								></p>
							</div>
						))
					) : (
						<p className="text-center font-medium text-lg pt-4">
							Hello! I&apos;m you&apos;re personal fashion desginer. I can help you
							design your wardrobe. Try asking me something
						</p>
					)}
				</div>
				<form
					onSubmit={submitForm}
					className="w-full px-12 py-4 flex flex-row justify-between gap-8"
				>
					<textarea
						type="text"
						placeholder="Send a message"
						className="w-full py-2 px-2 text-lg border-2 border-gray-200"
						value={message}
						onChange={e => setMessage(e.currentTarget.value)}
					/>
					<input
						type="submit"
						className="bg-blue-600 text-white text-xl shadow-lg rounded-xl font-medium px-6 py-2"
						value={loading ? "Sending... Please wait" : "Send"}
						disabled={loading}
					/>
				</form>
			</main>
		</>
	);
}
