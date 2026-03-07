"use client";

import { useState } from "react";
import { Send, CheckCircle } from "lucide-react";

export default function ContactPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !email.trim() || !message.trim()) return;

    setSending(true);
    // Simulate sending — replace with a real API call when ready
    await new Promise((r) => setTimeout(r, 1000));
    setSending(false);
    setSent(true);
    setName("");
    setEmail("");
    setMessage("");
  };

  if (sent) {
    return (
      <div className="max-w-lg mx-auto text-center py-16">
        <CheckCircle size={48} className="text-green-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-white mb-2">Message Sent!</h2>
        <p className="text-gray-400 text-sm mb-6">
          Thank you for reaching out to Bontor. We&apos;ll get back to you as soon as possible.
        </p>
        <button
          onClick={() => setSent(false)}
          className="px-5 py-2 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-sm transition-colors"
        >
          Send Another Message
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto justify-center">
     <p className="text-gray-100 text-sm lg:text-lg mb-6 mx-2 text-center">
        Have questions, feedback, or need support? Send us a message and the Bontor team will get back to you.
     </p>
      <div className="bg-[#111111] border border-[#2a2a2a] rounded-xl p-6">
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {/* Name */}
          <div>
            <label htmlFor="contact-name" className="block text-sm text-gray-300 mb-1 font-medium">
              Full Name
            </label>
            <input
              id="contact-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
              required
              className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-md px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
              style={{ boxShadow: 'none' }}
              onFocus={(e) => { e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)'; }}
              onBlur={(e) => { e.target.style.boxShadow = 'none'; }}
            />
          </div>

          {/* Email */}
          <div>
            <label htmlFor="contact-email" className="block text-sm text-gray-300 mb-1 font-medium">
              Email
            </label>
            <input
              id="contact-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-md px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
              style={{ boxShadow: 'none' }}
              onFocus={(e) => { e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)'; }}
              onBlur={(e) => { e.target.style.boxShadow = 'none'; }}
            />
          </div>

          {/* Message */}
          <div>
            <label htmlFor="contact-message" className="block text-sm text-gray-300 mb-1 font-medium">
              Message
            </label>
            <textarea
              id="contact-message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Write your message here..."
              required
              rows={5}
              className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-md px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors resize-none"
              style={{ boxShadow: 'none' }}
              onFocus={(e) => { e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)'; }}
              onBlur={(e) => { e.target.style.boxShadow = 'none'; }}
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={sending}
            className="flex items-center justify-center gap-2 w-full py-2.5 rounded-md bg-blue-700 hover:bg-blue-800 border border-blue-700 hover:border-blue-800 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium transition-colors"
          >
            {sending ? "Sending..." : "Send Message"}
            <Send size={14} />
          </button>
        </form>
      </div>
    </div>
  );
}
