import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold mb-4">Welcome to the Messenger App</h1>
      <div className="flex space-x-4">
        <Link href="/auth/login">
          <button className="bg-blue-500 text-white py-2 px-4 rounded">Login</button>
        </Link>
        <Link href="/auth/sign-up">
          <button className="bg-green-500 text-white py-2 px-4 rounded">Sign Up</button>
        </Link>
        <Link href="/chat">
          <button className="bg-gray-500 text-white py-2 px-4 rounded">Chat</button>
        </Link>
      </div>
    </div>
  );
}
