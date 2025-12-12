"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import {
  User,
  LogOut,
  ChevronDown,
  Edit,
  Search,
  Paperclip,
  ArrowUp,
} from "lucide-react";

export default function AgentPage() {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [hasToken, setHasToken] = useState<boolean | null>(null);
  const [user, setUser] = useState<{ name: string; email?: string } | null>(
    null
  );
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);
  const [chatHistory, setChatHistory] = useState<any[]>([]);

  useEffect(() => {
    // Check if user is authenticated via cookie
    const checkAuth = async () => {
      try {
        const response = await fetch("/api/auth/me");
        const data = await response.json();

        if (data.user) {
          setUser(data.user);
          setHasToken(true);
        } else {
          setHasToken(false);
        }
      } catch (error) {
        console.error("Auth check error:", error);
        setHasToken(false);
      }
    };

    checkAuth();
  }, []);

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

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    localStorage.setItem('just_logged_out', 'true');
    localStorage.removeItem('just_logged_in');
    window.location.href = "/landing";
  };

  return (
    <div className="min-h-screen text-white relative">
      {/* Ultravib image background with dark overlay */}
      <div
        className="fixed inset-x-0"
        style={{
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: "url(/image/Ultravib.png)",
          backgroundSize: "cover",
          backgroundPosition: "center center",
          backgroundRepeat: "no-repeat",
          filter: "brightness(0.8)",
          zIndex: 0,
          pointerEvents: "none",
        }}
      />

      {/* Header */}
      <header
        className="bg-white/2 backdrop-blur-md"
        style={{
          padding: "16px 0",
          minHeight: "4rem",
          position: "sticky",
          top: 0,
          zIndex: 100,
        }}
      >
        <div
          style={{ maxWidth: "1200px", margin: "0 auto", padding: "0 24px", height: '100%' }}
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
              <button
                onClick={() => router.push("/landing")}
                className="hover:opacity-80 transition-opacity"
                style={{
                  background: "transparent",
                  border: "none",
                  padding: 0,
                }}
              >
                <img
                  src="/image/Bontor-logo.png"
                  alt="Bontor"
                  className="h-5 md:h-[23px] w-auto"
                />
              </button>
            </div>

            {/* Navigation Links - Centered - Hidden on mobile */}
            <div
              className="hidden lg:flex items-center space-x-8"
              style={{ position: "absolute", left: "50%", transform: "translateX(-50%)" }}
            >
              <button
                onClick={() => router.push("/Input")}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Analyze
              </button>
              <button
                onClick={() => router.push("/dashboard")}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Dashboard
              </button>
              <button
                onClick={() => router.push("/university")}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                University
              </button>
              <button
                onClick={() => router.push("/agent")}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Agent
              </button>
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
              <button
                onClick={() => { router.push('/Input'); setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Analyze
              </button>
              <button
                onClick={() => { router.push('/dashboard'); setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Dashboard
              </button>
              <button
                onClick={() => { router.push('/university'); setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                University
              </button>
              <button
                onClick={() => { router.push('/agent'); setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Agent
              </button>
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

      {/* Main content area - ready for chatbot implementation */}
      <div className="relative z-10 flex min-h-screen">
        {/* Sidebar for chat history - background only */}
        <aside className="hidden md:block fixed left-0 top-18 w-64 bg-[#111111] border-r border-[#1f1f1f] h-[calc(100vh-4rem)] overflow-auto z-20">
          <div className="p-4">
            <button
              type="button"
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
                    <div key={idx} className="mt-2 px-1 py-1 text-sm text-gray-100 truncate">
                      {c.title || `Chat ${idx + 1}`}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </aside>
        {/* Main Content */}
        <div className="flex-1 md:ml-64">
          {/* Chatbot interface will go here */}
        </div>
        {/* Floating chat input (centered) */}
        <div className="fixed left-4 right-4 bottom-6 md:left-80 md:right-8 z-40">
          <div className="mx-auto max-w-full md:max-w-[900px]">
            <div className="w-full bg-[#111111] rounded-2xl p-3 py-[2px] shadow-lg border border-[#1f1f1f] focus-within:ring-1 focus-within:ring-blue-500 transition-all duration-200">
              <textarea
                placeholder="Ask agent a question..."
                className="w-full bg-[#111111] placeholder-gray-500 text-gray-200 px-4 py-3 rounded-lg focus:outline-none text-sm h-12 resize-none"
              />

              <div className="mt-3 flex items-center justify-between">
                <button className="p-2 text-gray-300 hover:text-white">
                  <Paperclip className="w-5 h-5" />
                </button>

                <button className="p-3 mx-2 my-2 bg-white/6 hover:bg-white/10 rounded-md">
                  <ArrowUp className="w-5 h-5 text-white" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

