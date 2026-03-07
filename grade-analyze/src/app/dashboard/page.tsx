"use client";

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import {
  User,
  LogOut,
  ChevronDown,
  LayoutDashboard,
  Mail,
  Clock,
  MessageSquare,
  ChevronRight,
  Pencil,
  Check,
  X,
  TrendingUp,
  Send,
} from 'lucide-react';
import PerformanceChart from '@/components/charts/PerformanceChart';
import ContactPage from './contact/ContactPage';

type ActiveSection = 'overview' | 'contact' | 'history' | 'chat-history';

interface AnalysisResult {
  subject_analysis?: Record<string, { score: number; normalized: number; strength: string }>;
}

export default function DashboardPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<{ name: string; email?: string } | null>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);

  // Sidebar state
  const [activeSection, setActiveSection] = useState<ActiveSection>('overview');
  const [historyOpen, setHistoryOpen] = useState(false);
  const [chatHistoryOpen, setChatHistoryOpen] = useState(true);

  // Edit name
  const [isEditingName, setIsEditingName] = useState(false);
  const [editNameValue, setEditNameValue] = useState('');
  const [savingName, setSavingName] = useState(false);
  const editInputRef = useRef<HTMLInputElement>(null);

  // Stats from localStorage/sessionStorage
  const [analysisCount, setAnalysisCount] = useState(0);
  const [chatCount, setChatCount] = useState(0);
  const [requestCount, setRequestCount] = useState(0);
  const [statsLoading, setStatsLoading] = useState(true);
  const [recentAnalysis, setRecentAnalysis] = useState<AnalysisResult | null>(null);
  const [chatHistory, setChatHistory] = useState<{ title: string }[]>([]);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch('/api/auth/me');
        const data = await response.json();
        if (data.user) {
          setUser(data.user);
        } else {
          router.push('/login');
        }
      } catch {
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };
    checkAuth();
  }, [router]);

  // Load stats from localStorage/sessionStorage
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('/api/auth/stats');
        if (res.ok) {
          const data = await res.json();
          setAnalysisCount(data.analysisCount ?? 0);
          setRequestCount(data.requestCount ?? 0);
        }
      } catch {
        // silently fail
      } finally {
        setStatsLoading(false);
      }
    };
    fetchStats();

    try {
      // Chat history from localStorage
      const storedChats = localStorage.getItem('chatHistory');
      if (storedChats) {
        const parsed = JSON.parse(storedChats);
        const validChats = parsed.filter((c: { messages?: unknown[] }) => c.messages && (c.messages as unknown[]).length > 0);
        setChatHistory(validChats);
        setChatCount(validChats.length);
      }

      // Recent analysis from sessionStorage
      const stored = sessionStorage.getItem('analysisResult');
      if (stored) {
        setRecentAnalysis(JSON.parse(stored));
      }
    } catch {
      // silently fail
    }
  }, []);

  // Close profile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setShowProfileMenu(false);
      }
    };
    if (showProfileMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showProfileMenu]);

  // Focus edit input when editing
  useEffect(() => {
    if (isEditingName && editInputRef.current) {
      editInputRef.current.focus();
    }
  }, [isEditingName]);

  const handleLogout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    localStorage.setItem('just_logged_out', 'true');
    localStorage.removeItem('just_logged_in');
    window.location.href = '/landing';
  };

  const handleStartEditName = () => {
    setEditNameValue(user?.name || '');
    setIsEditingName(true);
  };

  const handleSaveName = async () => {
    if (!editNameValue.trim() || editNameValue.trim() === user?.name) {
      setIsEditingName(false);
      return;
    }
    setSavingName(true);
    try {
      const res = await fetch('/api/auth/me', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: editNameValue.trim() }),
      });
      const data = await res.json();
      if (data.user) {
        setUser(data.user);
      }
    } catch {
      // silently fail
    } finally {
      setSavingName(false);
      setIsEditingName(false);
    }
  };

  const handleCancelEditName = () => {
    setIsEditingName(false);
    setEditNameValue('');
  };

  // Build chart data from recentAnalysis
  const hasAnalysisData = recentAnalysis?.subject_analysis && Object.keys(recentAnalysis.subject_analysis).length > 0;

  if (loading || statsLoading) {
    return (
      <div style={{
        display: 'flex', justifyContent: 'center', alignItems: 'center',
        minHeight: '100vh', padding: '40px 20px', position: 'relative'
      }}>
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          backgroundImage: "url(/image/Ultravib.png)", backgroundSize: 'cover',
          backgroundPosition: 'center center', backgroundRepeat: 'no-repeat',
          filter: 'brightness(0.9)', zIndex: 0, pointerEvents: 'none'
        }} />
        <div style={{ position: 'relative', zIndex: 10 }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '24px' }}>
            <svg className="logo-spin" width="80" height="80" viewBox="-30 -30 201 233" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block' }}>
              <g><path d="M110.464 0C127.032 0.000247877 140.464 13.4316 140.464 30V31.4922H92.9033V58.2891H49.9043V86.3154H0V30C0 13.4315 13.4315 1.61637e-06 30 0H110.464Z" fill="white" /></g>
              <g><path d="M30.5372 172.649C13.9687 172.67 0.453776 159.257 0.350835 142.689L0.341564 141.196L47.9011 141.134L47.7346 114.338L90.7336 114.282L90.5595 86.2549L140.464 86.1897L140.814 142.505C140.917 159.073 127.569 172.522 111 172.544L30.5372 172.649Z" fill="#3B82F6" /></g>
            </svg>
            <img src="/image/Bontor-logo.png" alt="Bontor" style={{ height: '30px', width: 'auto', display: 'block' }} />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen overflow-hidden text-white relative">
      {/* Background */}
      <div
        className="fixed inset-0"
        style={{
          backgroundImage: "url(/image/Ultravib.png)", backgroundSize: 'cover',
          backgroundPosition: 'center center', backgroundRepeat: 'no-repeat',
          filter: 'brightness(0.9)', zIndex: 0, pointerEvents: 'none'
        }}
      />

      {/* Header / Navbar */}
      <header className="bg-white/2 backdrop-blur-md relative z-50" style={{ padding: '16px 0', minHeight: '4rem', position: 'sticky', top: 0 }}>
        <div className="max-w-[1200px] 2xl:max-w-none mx-auto px-6 2xl:px-24 h-full">
          <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr auto', alignItems: 'center', height: '100%', position: 'relative' }}>
            {/* Logo + mobile hamburger */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <button
                onClick={() => setIsMenuOpen(true)}
                className="lg:hidden p-2 hover:bg-gray-800 rounded-md transition-colors"
                style={{ background: 'transparent', border: 'none' }}
                aria-label="Open menu"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 22 22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 5H3" /><path d="M21 12H9" /><path d="M21 19H7" />
                </svg>
              </button>
              <button onClick={() => router.push('/landing')} className="hover:opacity-80 transition-opacity" style={{ background: 'transparent', border: 'none', padding: 0 }}>
                <img src="/image/Bontor-logo.png" alt="Bontor" className="h-5 md:h-[23px] w-auto" />
              </button>
            </div>

            {/* Desktop Nav - Centered */}
            <div className="hidden lg:flex items-center space-x-8" style={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)' }}>
              {['Analyze', 'Dashboard', 'University', 'Agent'].map((label) => {
                const paths: Record<string, string> = { Analyze: '/Input', Dashboard: '/dashboard', University: '/university', Agent: '/agent' };
                return (
                  <button key={label} onClick={() => router.push(paths[label])}
                    className="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-gray-800 transition-colors">
                    {label}
                  </button>
                );
              })}
            </div>

            {/* Profile Menu */}
            <div style={{ display: 'flex', alignItems: 'center', justifySelf: 'end', gap: '8px', position: 'relative' }}>
              <div ref={profileMenuRef} style={{ position: 'relative' }}>
                <button
                  onClick={() => setShowProfileMenu(!showProfileMenu)}
                  className="flex items-center gap-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
                  style={{ fontSize: '14px' }}
                >
                  <User size={16} />
                  <span className="hidden sm:inline max-w-[120px] truncate">{user?.name ?? '\u00A0'}</span>
                  <ChevronDown size={14} style={{ transform: showProfileMenu ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }} />
                </button>
                {showProfileMenu && (
                  <div style={{ position: 'absolute', top: '100%', right: 0, marginTop: '8px', background: '#1f2937', border: '1px solid #374151', borderRadius: '8px', minWidth: '160px', boxShadow: '0 10px 25px rgba(0,0,0,0.5)', zIndex: 1000, overflow: 'hidden' }}>
                    <div style={{ padding: '8px 12px', borderBottom: '1px solid #374151' }}>
                      <p style={{ color: '#fff', fontSize: '14px', fontWeight: 600, margin: 0 }}>{user?.name || 'User'}</p>
                      {user?.email && <p style={{ color: '#9ca3af', fontSize: '12px', margin: '4px 0 0 0' }}>{user.email}</p>}
                    </div>
                    <button onClick={handleLogout} className="w-full flex items-center gap-3 px-4 py-3 text-white hover:bg-gray-700 transition-colors" style={{ fontSize: '14px', background: 'transparent', border: 'none', cursor: 'pointer', textAlign: 'left' }}>
                      <LogOut size={16} /> Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Sidebar Menu overlay */}
      {isMenuOpen && (
        <div className="fixed inset-0 z-[200] lg:hidden">
          <button className="absolute inset-0 bg-black/60 backdrop-blur-md" aria-label="Close menu" onClick={() => setIsMenuOpen(false)} />
          <aside
            className="absolute top-0 left-0 h-full w-72 max-w-[80%] text-white border-r border-white/10 shadow-2xl"
            style={{ backgroundImage: "linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(/image/Ultravib.png)", backgroundSize: 'cover', backgroundPosition: 'center' }}
          >
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <span className="text-base font-semibold tracking-wide uppercase">Menu</span>
              <button onClick={() => setIsMenuOpen(false)} className="p-1 text-white/80 hover:text-white transition-colors" aria-label="Close menu">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
            <div className="flex flex-col gap-6 px-5 py-6 text-sm">
              {[['Analyze', '/Input'], ['Dashboard', '/dashboard'], ['University', '/university'], ['Agent', '/agent']].map(([label, path]) => (
                <button key={label} onClick={() => { router.push(path); setIsMenuOpen(false); }} className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors">{label}</button>
              ))}
            </div>
            <div className="mt-5 px-5 pb-8">
              <div className="mb-3">
                <p className="text-white font-semibold text-sm">{user?.name}</p>
                {user?.email && <p className="text-white/60 text-xs mt-1">{user.email}</p>}
              </div>
              <button onClick={() => { handleLogout(); setIsMenuOpen(false); }} className="w-full justify-center px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600">Logout</button>
            </div>
          </aside>
        </div>
      )}

      {/* Page body */}
      <div className="relative z-10 flex" style={{ height: 'calc(100vh - 4rem)' }}>

        {/* Desktop Sidebar */}
        <aside className="hidden md:flex flex-col w-64 flex-shrink-0 bg-[#111111] border-r border-[#1f1f1f] overflow-y-auto z-20">
          <div className="p-7">

            {/* User info section */}
            <div className="pt-5 pb-4 mb-4 border-b border-gray-700">
              {isEditingName ? (
                <div className="flex items-center gap-1">
                  <input
                    ref={editInputRef}
                    value={editNameValue}
                    onChange={(e) => setEditNameValue(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') handleSaveName(); if (e.key === 'Escape') handleCancelEditName(); }}
                    className="bg-[#1f1f1f] text-white text-sm font-semibold rounded px-2 py-0.5 border border-blue-500 focus:outline-none w-full"
                    maxLength={100}
                    disabled={savingName}
                  />
                  <button onClick={handleSaveName} disabled={savingName} className="text-green-400 hover:text-green-500 flex-shrink-0 p-0.5">
                    <Check size={14} />
                  </button>
                  <button onClick={handleCancelEditName} disabled={savingName} className="text-red-400 hover:text-red-500 flex-shrink-0 p-0.5">
                    <X size={14} />
                  </button>
                </div>
              ) : (
                <div className="flex items-center gap-1.5 min-w-0">
                  <p className="text-white font-semibold text-sm truncate">{user?.name}</p>
                  <button onClick={handleStartEditName} className="text-gray-400 hover:text-white flex-shrink-0 p-0.5 rounded hover:bg-white/5 transition-colors" title="Edit name">
                    <Pencil size={12} />
                  </button>
                </div>
              )}
              {user?.email && <p className="text-gray-400 text-xs mt-0.5 truncate">{user.email}</p>}
            </div>

            {/* Nav items */}
            <nav className="flex flex-col gap-1">
              {/* Overview */}
              <button
                onClick={() => setActiveSection('overview')}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors text-left text-gray-100 hover:bg-gray-800 ${activeSection === 'overview' ? 'bg-gray-800' : ''}`}
              >
                <LayoutDashboard size={16} className="flex-shrink-0" />
                <span>Overview</span>
              </button>

              {/* Contact Us */}
              <button
                onClick={() => setActiveSection('contact')}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors text-left text-gray-100 hover:bg-gray-800 ${activeSection === 'contact' ? 'bg-gray-800' : ''}`}
              >
                <Mail size={16} className="flex-shrink-0" />
                <span>Contact Us</span>
              </button>

              {/* History (expandable) */}
              <button
                onClick={() => setHistoryOpen(!historyOpen)}
                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm text-gray-100 hover:bg-gray-800 transition-colors text-left"
              >
                <Clock size={16} className="flex-shrink-0" />
                <span className="flex-1">History</span>
                <ChevronRight size={14} className={`flex-shrink-0 transition-transform ${historyOpen ? 'rotate-90' : ''}`} />
              </button>
              {historyOpen && (
                <div className="ml-7 flex flex-col gap-0.5">
                  <p className="text-xs text-gray-500 px-3 py-1">No history yet</p>
                </div>
              )}

              {/* Chat History (expandable) */}
              <button
                onClick={() => setChatHistoryOpen(!chatHistoryOpen)}
                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm text-gray-100 hover:bg-gray-800 transition-colors text-left"
              >
                <MessageSquare size={16} className="flex-shrink-0" />
                <span className="flex-1">Chat History</span>
                <ChevronRight size={14} className={`flex-shrink-0 transition-transform ${chatHistoryOpen ? 'rotate-90' : ''}`} />
              </button>
              {chatHistoryOpen && (
                <div className="ml-7 flex flex-col gap-0.5">
                  {chatHistory.length === 0 ? (
                    <p className="text-xs text-gray-500 px-3 py-1">No chats yet</p>
                  ) : (
                    chatHistory.map((c, i) => (
                      <button
                        key={i}
                        onClick={() => router.push('/agent')}
                        className="text-left text-xs text-gray-100 hover:bg-gray-800 px-3 py-1.5 rounded transition-colors truncate"
                      >
                        {c.title || `Chat ${i + 1}`}
                      </button>
                    ))
                  )}
                </div>
              )}
            </nav>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto scrollbar-hide">
          <div className="p-6 md:p-8">

            {/* Dashboard label */}
            <div className="flex items-center justify-center mb-6">
              <div className="inline-flex items-center gap-2 px-3 py-2 rounded-md bg-[#1a1a1a] border border-[#2a2a2a]">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                <span className="text-sm text-gray-400">{activeSection === 'contact' ? 'Contact Us' : 'Dashboard'}</span>
              </div>
            </div>

            {/* Overview section */}
            {activeSection === 'overview' && (
              <div>
                {/* Stats cards */}
                <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-8 px-2 lg:px-20">
                  {/* Analysis */}
                  <div className="bg-[#111111] border border-[#2a2a2a] rounded-xl p-3 lg:p-5">
                    <div className="flex items-center gap-1.5 lg:gap-2 mb-2 lg:mb-3">
                      <div className="p-1 lg:p-1.5">
                        <TrendingUp size={18} className="text-green-400"/>
                      </div>
                      <p className="text-xs lg:text-lg text-white tracking-wide leading-tight">Analysis <span className="text-xs lg:text-sm text-gray-400">(Total)</span></p>
                    </div>
                    <p className="text-xl lg:text-3xl font-bold text-white ml-1">{analysisCount}</p>
                  </div>

                  {/* Chats */}
                  <div className="bg-[#111111] border border-[#2a2a2a] rounded-xl p-3 lg:p-5">
                    <div className="flex items-center gap-1.5 lg:gap-2 mb-2 lg:mb-3">
                      <div className="p-1 lg:p-1.5">
                        <MessageSquare size={18} className="text-blue-400" />
                      </div>
                      <p className="text-xs lg:text-lg text-white tracking-wide leading-tight">Chats <span className="text-xs lg:text-sm text-gray-400">(Total)</span></p>
                    </div>
                    <p className="text-xl lg:text-3xl font-bold text-white ml-1">{chatCount}</p>
                  </div>

                  {/* Requests */}
                  <div className="col-span-2 lg:col-span-1 bg-[#111111] border border-[#2a2a2a] rounded-xl p-3 lg:p-5">
                    <div className="flex items-center gap-1.5 lg:gap-2 mb-2 lg:mb-3">
                      <div className="p-1 lg:p-1.5">
                        <Send size={18} className="text-blue-400" />
                      </div>
                      <p className="text-xs lg:text-lg text-white tracking-wide leading-tight">Requests <span className="text-xs lg:text-sm text-gray-400">(Total)</span></p>
                    </div>
                    <p className="text-xl lg:text-3xl font-bold text-white ml-1">0</p>
                  </div>
                </div>

                {/* Recent Analysis */}
                
              </div>
            )}

            {/* Contact Us section */}
            {activeSection === 'contact' && <ContactPage />}

          </div>
        </main>
      </div>
    </div>
  );
}


