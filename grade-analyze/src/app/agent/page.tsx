"use client";

import { useState, useEffect, useRef, useLayoutEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import {
  User,
  LogOut,
  ChevronDown,
  Edit,
  Search,
  Paperclip,
  ArrowUp,
  Bot,
  BotMessageSquare,
  Trash2,
} from "lucide-react";

export default function AgentPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <AgentPageContent />
    </Suspense>
  );
}

function AgentPageContent() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<{ name: string; email?: string } | null>(
    null
  );
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);
  const [chatHistory, setChatHistory] = useState<{ id: number; title: string; messages: { role: 'user' | 'assistant'; content: string }[] }[]>([]);
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [activeChatIndex, setActiveChatIndex] = useState<number | null>(null);
  const chatAreaRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const inputContainerRef = useRef<HTMLDivElement>(null);

  // Unified initialization to load both User and Chat History before showing the page
  useEffect(() => {
    const initPage = async () => {
      try {
        // Run auth check and chat history loading in parallel
        const [authRes, historyRes] = await Promise.all([
          fetch("/api/auth/me"),
          fetch("/api/agent/sessions")
        ]);

        // Process Auth
        if (authRes.ok) {
          const authData = await authRes.json();
          if (authData.user) {
            setUser(authData.user);
          }
        } else {
        }

        // Process Chat History
        if (historyRes.ok) {
          const historyData = await historyRes.json();
          const sessions = historyData.sessions.map((s: { id: number; title: string; messages: { role: string; content: string }[] }) => ({
            id: s.id,
            title: s.title,
            messages: s.messages.map((m: { role: string; content: string }) => ({
              role: m.role as 'user' | 'assistant',
              content: m.content,
            })),
          }));
          setChatHistory(sessions);
        }
      } catch (error) {
        console.error("Initialization error:", error);
      } finally {
        setLoading(false);
      }
    };

    initPage();
  }, []);

  // Handle sessionId from query search parameters
  const searchParams = useSearchParams();
  useEffect(() => {
    const sessionIdParam = searchParams.get('sessionId');
    if (sessionIdParam && chatHistory.length > 0) {
      const id = parseInt(sessionIdParam);
      const sessionIndex = chatHistory.findIndex(s => s.id === id);
      if (sessionIndex !== -1) {
        setActiveChatIndex(sessionIndex);
        setMessages(chatHistory[sessionIndex].messages);
        setActiveSessionId(id);
      }
    }
  }, [searchParams, chatHistory]);

  // Close profile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        profileMenuRef.current &&
        !profileMenuRef.current.contains(event.target as Node)
      ) {
        setShowProfileMenu(false);
      }
    };

    if (showProfileMenu) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showProfileMenu]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [messages]);

  // Auto-resize textarea and update bottom padding
  useLayoutEffect(() => {
    if (textareaRef.current) {
      // Reset height to auto to get the correct scrollHeight
      textareaRef.current.style.height = 'auto';
      
      const scrollHeight = textareaRef.current.scrollHeight;
      // Enforce min height of 60px (matching the CSS min-h-[60px])
      const newHeight = Math.max(scrollHeight, 60);
      
      textareaRef.current.style.height = `${Math.min(newHeight, 200)}px`;
    }

    // Measure input container height to adjust chat padding
    if (inputContainerRef.current) {
      // Add a small buffer (e.g., 20px)
    }
  }, [inputValue]);
  
  const [isLoading, setIsLoading] = useState(false);
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = { role: 'user' as const, content: inputValue };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the Gemini API with sessionId for DB persistence
      const res = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages,
          sessionId: activeSessionId,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Failed to get response');
      }

      const assistantMessage = { role: 'assistant' as const, content: data.message };
      const finalMessages = [...newMessages, assistantMessage];
      setMessages(finalMessages);

      // Update local chat history state
      const returnedSessionId = data.sessionId as number;

      if (!activeSessionId) {
        // New session was created by the API
        const newTitle = inputValue.slice(0, 30) + (inputValue.length > 30 ? '...' : '');
        setActiveSessionId(returnedSessionId);
        setChatHistory(prev => [...prev, { id: returnedSessionId, title: newTitle, messages: finalMessages }]);
        setActiveChatIndex(chatHistory.length);
      } else {
        // Update existing session in local state
        setChatHistory(prev =>
          prev.map(s => s.id === activeSessionId ? { ...s, messages: finalMessages } : s)
        );
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Something went wrong. Please try again.';
      const assistantMessage = { role: 'assistant' as const, content: `Error: ${errorMessage}` };
      const finalMessages = [...newMessages, assistantMessage];
      setMessages(finalMessages);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setActiveChatIndex(null);
    setActiveSessionId(null);
  };

  const handleLoadChat = (chatIndex: number) => {
    const selectedChat = chatHistory[chatIndex];
    if (selectedChat) {
      setMessages(selectedChat.messages);
      setActiveChatIndex(chatIndex);
      setActiveSessionId(selectedChat.id);
    }
  };

  const handleDeleteChat = async (chatIndex: number, e: React.MouseEvent) => {
    e.stopPropagation();

    const session = chatHistory[chatIndex];
    if (!session) return;

    // Delete from database
    try {
      await fetch(`/api/agent/sessions/${session.id}`, { method: 'DELETE' });
    } catch (error) {
      console.error('Failed to delete chat session:', error);
    }

    // Update local state
    setChatHistory(prev => prev.filter((_, idx) => idx !== chatIndex));

    if (activeChatIndex === chatIndex) {
      setMessages([]);
      setActiveChatIndex(null);
      setActiveSessionId(null);
    } else if (activeChatIndex !== null && activeChatIndex > chatIndex) {
      setActiveChatIndex(activeChatIndex - 1);
    }
  };

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    localStorage.setItem('just_logged_out', 'true');
    localStorage.removeItem('just_logged_in');
    window.location.href = "/landing";
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        padding: '40px 20px',
        position: 'relative'
      }}>
        {/* Ultravib image background */}
        <div
          style={{ 
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundImage: "url(/image/Ultravib.png)",
            backgroundSize: 'cover',
            backgroundPosition: 'center center',
            backgroundRepeat: 'no-repeat',
            filter: 'brightness(0.9)',
            zIndex: 0,
            pointerEvents: 'none'
          }}
        />
        <div style={{ position: 'relative', zIndex: 10 }}>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '24px'
          }}>
            <svg className="logo-spin" width="80" height="80" viewBox="-30 -30 201 233" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block' }}>
              <g>
                <path d="M110.464 0C127.032 0.000247877 140.464 13.4316 140.464 30V31.4922H92.9033V58.2891H49.9043V86.3154H0V30C0 13.4315 13.4315 1.61637e-06 30 0H110.464Z" fill="white"/>
              </g>
              <g>
                <path d="M30.5372 172.649C13.9687 172.67 0.453776 159.257 0.350835 142.689L0.341564 141.196L47.9011 141.134L47.7346 114.338L90.7336 114.282L90.5595 86.2549L140.464 86.1897L140.814 142.505C140.917 159.073 127.569 172.522 111 172.544L30.5372 172.649Z" fill="#3B82F6"/>
              </g>
            </svg>
            <img 
              src="/image/Bontor-logo.png" 
              alt="Bontor" 
              style={{ 
                height: '30px',
                width: 'auto',
                display: 'block'
              }}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden text-white relative bg-black">
      {/* Ultravib image background with dark overlay */}
      <div
        className="fixed inset-0"
        style={{
          backgroundImage: "url(/image/Ultravib.png)",
          backgroundSize: "cover",
          backgroundPosition: "center center",
          backgroundRepeat: "no-repeat",
          filter: "brightness(0.9)",
          zIndex: 0,
          pointerEvents: "none",
        }}
      />

      {/* Header */}
      <header
        className="bg-white/2 backdrop-blur-md flex-shrink-0 relative z-50"
        style={{
          padding: "16px 0",
          minHeight: "4rem",
        }}
      >
        <div
          className="max-w-[1200px] 2xl:max-w-none mx-auto px-6 2xl:px-24 h-full"
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "auto 1fr auto",
              alignItems: "center",
              height: '100%',
              position: 'relative'
            }}
          >
            {/* Logo and mobile menu */}
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <button
                onClick={() => setIsMenuOpen(true)}
                className="lg:hidden p-2 hover:bg-gray-800 rounded-md transition-colors"
                style={{ background: 'transparent', border: 'none' }}
                aria-label="Open menu"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 22 22"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M21 5H3" />
                  <path d="M21 12H9" />
                  <path d="M21 19H7" />
                </svg>
              </button>
              <Link href="/landing" className="hover:opacity-80 transition-opacity" style={{ padding: 0 }}>
                <img
                  src="/image/Bontor-logo.png"
                  alt="Bontor"
                  className="h-5 md:h-[23px] w-auto"
                />
              </Link>
            </div>

            {/* Navigation Links - Centered - Hidden on mobile */}
            <div
              className="hidden lg:flex items-center space-x-8"
              style={{ position: "absolute", left: "50%", transform: "translateX(-50%)" }}
            >
              <Link
                href="/Input"
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Analyze
              </Link>
              <Link
                href="/dashboard"
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/university"
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                University
              </Link>
              <Link
                href="/agent"
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Agent
              </Link>
            </div>

            {/* Profile Menu */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifySelf: "end",
                gap: "8px",
                position: "relative",
              }}
            >
              <div ref={profileMenuRef} style={{ position: "relative" }}>
                <button
                  onClick={() => setShowProfileMenu(!showProfileMenu)}
                  className="flex items-center gap-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
                  style={{
                    fontSize: "14px",
                  }}
                >
                  <User size={16} />
                  <span className="hidden sm:inline max-w-[120px] truncate">
                    {user?.name ?? '\u00A0'}
                  </span>
                  <ChevronDown
                    size={14}
                    style={{
                      transform: showProfileMenu
                        ? "rotate(180deg)"
                        : "rotate(0deg)",
                      transition: "transform 0.2s",
                    }}
                  />
                </button>

                {/* Dropdown Menu */}
                {showProfileMenu && (
                  <div
                    style={{
                      position: "absolute",
                      top: "100%",
                      right: 0,
                      marginTop: "8px",
                      background: "#1f2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                      minWidth: "160px",
                      boxShadow: "0 10px 25px rgba(0, 0, 0, 0.5)",
                      zIndex: 1000,
                      overflow: "hidden",
                    }}
                  >
                    <div
                      style={{
                        padding: "8px 12px",
                        borderBottom: "1px solid #374151",
                      }}
                    >
                      <p
                        style={{
                          color: "#ffffff",
                          fontSize: "14px",
                          fontWeight: "600",
                          margin: 0,
                        }}
                      >
                        {user?.name || "User"}
                      </p>
                      {user?.email && (
                        <p
                          style={{
                            color: "#9ca3af",
                            fontSize: "12px",
                            margin: "4px 0 0 0",
                          }}
                        >
                          {user.email}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-4 py-3 text-white hover:bg-gray-700 transition-colors"
                      style={{
                        fontSize: "14px",
                        background: "transparent",
                        border: "none",
                        cursor: "pointer",
                        textAlign: "left",
                      }}
                    >
                      <LogOut size={16} />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Sidebar Menu */}
      {isMenuOpen && (
        <div className="fixed inset-0 z-[200] lg:hidden">
          <button
            className="absolute inset-0 bg-black/60 backdrop-blur-md"
            aria-label="Close menu"
            onClick={() => setIsMenuOpen(false)}
          />
          <aside
            className="absolute top-0 left-0 h-full w-72 max-w-[80%] text-white border-r border-white/10 shadow-2xl"
            style={{
              backgroundImage:
                "linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(/image/Ultravib.png)",
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          >
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <span className="text-base font-semibold tracking-wide uppercase">
                Menu
              </span>
              <button
                onClick={() => setIsMenuOpen(false)}
                className="p-1 text-white/80 hover:text-white transition-colors"
                aria-label="Close menu"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
            <div className="flex flex-col gap-6 px-5 py-6 text-sm">
              <Link
                href="/Input"
                onClick={() => setIsMenuOpen(false)}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Analyze
              </Link>
              <Link
                href="/dashboard"
                onClick={() => setIsMenuOpen(false)}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/university"
                onClick={() => setIsMenuOpen(false)}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                University
              </Link>
              <Link
                href="/agent"
                onClick={() => setIsMenuOpen(false)}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Agent
              </Link>
            </div>
            <div className="mt-5 px-5 pb-8">
              <div className="mb-3">
                <p className="text-white font-semibold text-sm">{user?.name}</p>
                {user?.email && (
                  <p className="text-white/60 text-xs mt-1">{user.email}</p>
                )}
              </div>
              <button
                onClick={() => { handleLogout(); setIsMenuOpen(false); }}
                className="w-full justify-center px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
              >
                Logout
              </button>
            </div>
          </aside>
        </div>
      )}

      {/* Mobile Chat Sidebar Overlay */}
      {isSidebarOpen && (
        <div className="md:hidden fixed inset-0 z-[180]">
          <button className="absolute inset-0 bg-black/60 backdrop-blur-sm" aria-label="Close sidebar" onClick={() => setIsSidebarOpen(false)} />
          <aside className="absolute top-0 left-0 h-full w-72 max-w-[85%] bg-[#111111] border-r border-[#1f1f1f] overflow-y-auto shadow-2xl">
            <div className="p-4">
              <button type="button" onClick={() => { handleNewChat(); setIsSidebarOpen(false); }} className="w-full flex items-center gap-3 px-2 py-2 rounded-md hover:bg-white/5 transition-colors text-gray-100">
                <Edit className="w-4 h-4" /><span className="text-sm text-white">New chat</span>
              </button>
              <button type="button" className="w-full flex items-center gap-3 px-2 py-2 mt-2 rounded-md hover:bg-white/5 transition-colors text-gray-100">
                <Search className="w-4 h-4" /><span className="text-sm text-white">Search chats</span>
              </button>
              <div className="mt-4 border-t border-gray-700 pt-3 px-2">
                <p className="text-xs text-gray-400 uppercase tracking-wide">Chat history</p>
                {chatHistory.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-8 px-2 text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5"><path strokeLinecap="round" strokeLinejoin="round" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" /></svg>
                    <p className="text-sm text-gray-200 font-semibold">No chats yet</p>
                    <p className="text-xs text-gray-400 mt-2">Start a new chat to see it here.</p>
                  </div>
                ) : (
                  <div>
                    {chatHistory.map((c, idx) => (
                      <div key={idx} className="group relative mt-2 px-3 py-2 text-sm text-gray-100 hover:bg-gray-800 rounded-md transition-colors">
                        <button onClick={() => { handleLoadChat(idx); setIsSidebarOpen(false); }} className="w-full text-left truncate pr-8">{c.title || `Chat ${idx + 1}`}</button>
                        <button onClick={(e) => handleDeleteChat(idx, e)} className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 opacity-0 group-hover:opacity-100 transition-all duration-200" title="Delete chat">
                          <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-400" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </aside>
        </div>
      )}
      <div className="relative z-10 flex flex-1 overflow-hidden">
        {/* Sidebar for chat history */}
        <aside className="hidden md:flex flex-col w-64 flex-shrink-0 bg-[#111111] border-r border-[#1f1f1f] overflow-y-auto z-20">
          <div className="p-4">
            <button
              type="button"
              onClick={handleNewChat}
              className="w-full flex items-center gap-3 px-2 py-2 rounded-md hover:bg-white/5 transition-colors text-gray-100"
            >
              <Edit className="w-4 h-4" />
              <span className="text-sm text-white">New chat</span>
            </button>

            <button
              type="button"
              className="w-full flex items-center gap-3 px-2 py-2 mt-2 rounded-md hover:bg-white/5 transition-colors text-gray-100"
            >
              <Search className="w-4 h-4" />
              <span className="text-sm text-white">Search chats</span>
            </button>

            <div className="mt-4 border-t border-gray-700 pt-3 px-2">
              <p className="text-xs text-gray-400 uppercase tracking-wide">Chat history</p>

              {chatHistory.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-8 px-2 text-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
                  </svg>
                  <p className="text-sm text-gray-200 font-semibold">No chats yet</p>
                  <p className="text-xs text-gray-400 mt-2">Start a new chat to see it here.</p>
                </div>
              ) : (
                <div>
                  {/* Chat items */}
                  {chatHistory.map((c, idx) => (
                    <div
                      key={idx}
                      className="group relative mt-2 px-3 py-2 text-sm text-gray-100 hover:bg-gray-800 rounded-md transition-colors"
                    >
                      <button
                        onClick={() => handleLoadChat(idx)}
                        className="w-full text-left truncate pr-8"
                      >
                        {c.title || `Chat ${idx + 1}`}
                      </button>
                      <button
                        onClick={(e) => handleDeleteChat(idx, e)}
                        className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 opacity-0 group-hover:opacity-100 transition-all duration-200"
                        title="Delete chat"
                      >
                        <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-400" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </aside>
        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div 
            ref={chatAreaRef} 
            className={`flex-1 p-4 px-6 flex flex-col overflow-y-auto scrollbar-hide`}
          >
            {messages.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center text-gray-200">
                <Bot className="w-16 h-16 text-blue-500 mb-6" />
                <p className="text-center text-lg">Ask me about major and skills that you want to prepare for the major</p>
              </div>
            ) : (
              <div className="max-w-[900px] mx-auto w-full space-y-4 pb-4">
                {messages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg break-words whitespace-pre-wrap ${
                      msg.role === 'user' ? 'bg-gray-800 text-white' : 'bg-gray-800 text-white'
                    }`}>
                      {msg.content}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-800 text-white px-4 py-3 rounded-lg flex items-center gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Chat input - anchored to bottom */}
          <div 
            ref={inputContainerRef}
            className="flex-shrink-0 p-4 pb-6 bg-gradient-to-t from-black via-black/80 to-transparent"
          >
            <div className="mx-auto max-w-full md:max-w-[900px] relative">
              {/* Mobile sidebar toggle - overlaid top-right of input, hidden on desktop */}
              <button
                onClick={() => setIsSidebarOpen(true)}
                className="md:hidden absolute -top-14 right-0 z-[150] flex items-center justify-center w-12 h-12 rounded-full bg-gray-800 border border-gray-600 text-white shadow-lg hover:bg-gray-700 transition-colors"
                aria-label="Open chat history"
              >
                <BotMessageSquare size={20} />
              </button>
              <div className="w-full bg-[#111111]/90 backdrop-blur-md rounded-2xl p-3 py-[2px] shadow-lg border border-[#1f1f1f] focus-within:ring-1 focus-within:ring-blue-500 transition-all duration-200">
                <textarea
                  ref={textareaRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  disabled={isLoading}
                  placeholder={isLoading ? "Waiting for response..." : "Ask agent a question..."}
                  className="w-full bg-[#111111] placeholder-gray-500 text-gray-200 px-4 py-3 rounded-lg focus:outline-none text-sm min-h-[60px] max-h-[200px] resize-none overflow-y-auto custom-scrollbar disabled:opacity-50"
                />
                <div className="mt-3 flex items-center justify-between">
                  <button className="p-2 text-gray-300 hover:text-white">
                    <Paperclip className="w-5 h-5" />
                  </button>
                  <button onClick={handleSend} disabled={isLoading || !inputValue.trim()} className="p-3 mx-2 my-2 bg-white/6 hover:bg-white/10 rounded-md disabled:opacity-30 disabled:cursor-not-allowed">
                    <ArrowUp className="w-5 h-5 text-white" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}