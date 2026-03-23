"use client";

import { useState, useEffect, useRef, createContext, useContext } from 'react';
import { AnalysisResult } from '../../types';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
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
  Trash2,
} from 'lucide-react';

// Analysis history item shape from the API
interface AnalysisHistoryItem {
  id: number;
  interestText: string;
  majors: unknown;
  careers: unknown;
  universities: unknown;
  skill_gaps: unknown;
  subject_analysis: unknown;
  createdAt: string;
}

// Define a context for sharing dashboard stats
interface DashboardContextType {
  analysisCount: number;
  chatCount: number;
  requestCount: number;
  recentAnalysis: AnalysisResult | null;
  statsLoading: boolean;
  analysisHistory: AnalysisHistoryItem[];
  selectedHistoryId: number | null;
  setSelectedHistoryId: (id: number | null) => void;
}

const DashboardContext = createContext<DashboardContextType | undefined>(undefined);

export function useDashboard() {
  const context = useContext(DashboardContext);
  if (context === undefined) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
}

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [loading, setLoading] = useState(true);
  const [statsLoading, setStatsLoading] = useState(true);
  const [analysisCount, setAnalysisCount] = useState(0);
  const [chatCount, setChatCount] = useState(0);
  const [requestCount, setRequestCount] = useState(0);
  const [recentAnalysis, setRecentAnalysis] = useState<AnalysisResult | null>(null);
  const [user, setUser] = useState<{ name: string; email?: string } | null>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);

  const activeSection = pathname === '/contact' ? 'contact' : pathname === '/history' ? 'history' : 'overview';

  // Analysis history from DB
  const [analysisHistory, setAnalysisHistory] = useState<AnalysisHistoryItem[]>([]);
  const [selectedHistoryId, setSelectedHistoryId] = useState<number | null>(null);
  const [historyVisibleCount, setHistoryVisibleCount] = useState(5);

  const handleSelectHistory = (id: number) => {
    setSelectedHistoryId(id);
    setIsSidebarOpen(false);
    router.push('/history');
  };

  const handleDeleteHistory = async (e: React.MouseEvent, id: number) => {
    e.preventDefault();
    e.stopPropagation();

    if (!confirm('Are you sure you want to delete this analysis?')) return;

    try {
      console.log(`[Client] Deleting history item: ${id}`);
      const res = await fetch(`/api/analysis-history/${id}?t=${Date.now()}`, { 
        method: 'DELETE',
        cache: 'no-store'
      });
      
      if (res.ok) {
        console.log(`[Client] Delete successful for ${id}. Refreshing history...`);
        // Fetch latest history to ensure UI is in sync with database
        const historyRes = await fetch(`/api/analysis-history?t=${Date.now()}`, { 
          cache: 'no-store' 
        });
        
        if (historyRes.ok) {
          const historyData = await historyRes.json();
          setAnalysisHistory(historyData.history || []);
          console.log(`[Client] History refreshed. Current count: ${historyData.history?.length}`);
        }
        
        // If the deleted item was selected, deselect it
        if (selectedHistoryId === id) {
          setSelectedHistoryId(null);
        }

        // Re-fetch stats without cache
        const statsRes = await fetch(`/api/stats?t=${Date.now()}`, { 
          cache: 'no-store' 
        });
        if (statsRes.ok) {
          const statsData = await statsRes.json();
          setAnalysisCount(statsData.analysisCount ?? 0);
          setChatCount(statsData.chatCount ?? 0);
          setRequestCount(statsData.requestCount ?? 0);
        }
      } else {
        const errData = await res.json().catch(() => ({}));
        alert(`Failed to delete history: ${errData.error || res.statusText || res.status}`);
      }
    } catch (err) {
      console.error('Delete error:', err);
      alert('Error deleting history. Check console for details.');
    }
  };
  
  // Sidebar state
  const [historyOpen, setHistoryOpen] = useState(false);
  const [chatHistoryOpen, setChatHistoryOpen] = useState(true);

  // Edit name
  const [isEditingName, setIsEditingName] = useState(false);
  const [editNameValue, setEditNameValue] = useState('');
  const [savingName, setSavingName] = useState(false);
  const editInputRef = useRef<HTMLInputElement>(null);
  const editInputRefMobile = useRef<HTMLInputElement>(null);

  // Chat History from DB
  const [chatSessions, setChatSessions] = useState<{ id: number; title: string; updatedAt: string }[]>([]);

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

  // Fetch stats, recent analysis, and history at layout level for consistency
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsRes, recentRes, historyRes] = await Promise.all([
          fetch('/api/stats'),
          fetch('/api/recent-analysis'),
          fetch('/api/analysis-history')
        ]);

        if (statsRes.ok) {
          const data = await statsRes.json();
          setAnalysisCount(data.analysisCount ?? 0);
          setChatCount(data.chatCount ?? 0);
          setRequestCount(data.requestCount ?? 0);
        }

        if (recentRes.ok) {
          const data = await recentRes.json();
          if (data.analysis) {
            setRecentAnalysis(data.analysis);
          }
        }

        if (historyRes.ok) {
          const data = await historyRes.json();
          if (Array.isArray(data.history)) {
            setAnalysisHistory(data.history);
          }
        }

        // Load chat history from DB
        const chatSessionsRes = await fetch('/api/agent/sessions');
        if (chatSessionsRes.ok) {
          const chatData = await chatSessionsRes.json();
          if (Array.isArray(chatData.sessions)) {
            setChatSessions(chatData.sessions.map((s: { id: number; title: string; updatedAt: string }) => ({
              id: s.id,
              title: s.title,
              updatedAt: s.updatedAt
            })));
          }
        }
      } catch {
        // silently fail
      } finally {
        setStatsLoading(false);
      }
    };
    fetchDashboardData();
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

  // Focus edit input when editing (mobile or desktop)
  useEffect(() => {
    if (isEditingName) {
      (editInputRefMobile.current ?? editInputRef.current)?.focus();
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
              <Link href="/landing" className="hover:opacity-80 transition-opacity">
                <img src="/image/Bontor-logo.png" alt="Bontor" className="h-5 md:h-[23px] w-auto" />
              </Link>
            </div>

            {/* Desktop Nav - Centered */}
            <div className="hidden lg:flex items-center space-x-8" style={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)' }}>
              {[['Analyze', '/Input'], ['Dashboard', '/dashboard'], ['University', '/university'], ['Agent', '/agent']].map(([label, path]) => (
                <Link key={label} href={path}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-gray-800 transition-colors">
                  {label}
                </Link>
              ))}
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
                <Link key={label} href={path} onClick={() => setIsMenuOpen(false)} className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors">{label}</Link>
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

      {/* Mobile FAB - bottom left, hidden on desktop */}
      <button
        onClick={() => setIsSidebarOpen(true)}
        className="md:hidden fixed bottom-6 left-6 z-[150] flex items-center justify-center w-12 h-12 rounded-full bg-gray-800 border border-gray-600 text-white shadow-lg hover:bg-gray-700 transition-colors"
        aria-label="Open sidebar"
      >
        <LayoutDashboard size={20} />
      </button>

      {/* Mobile Dashboard Sidebar Overlay */}
      {isSidebarOpen && (
        <div className="md:hidden fixed inset-0 z-[180]">
          <button className="absolute inset-0 bg-black/60 backdrop-blur-sm" aria-label="Close sidebar" onClick={() => setIsSidebarOpen(false)} />
          <aside className="absolute top-0 left-0 h-full w-72 max-w-[85%] bg-[#111111] border-r border-[#1f1f1f] overflow-y-auto shadow-2xl">
            <div className="p-7">
              <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-700">
                <div className="min-w-0 flex-1">
                  {isEditingName ? (
                    <div className="flex items-center gap-1">
                      <input
                        ref={editInputRefMobile}
                        value={editNameValue}
                        onChange={(e) => setEditNameValue(e.target.value)}
                        onKeyDown={(e) => { if (e.key === 'Enter') handleSaveName(); if (e.key === 'Escape') handleCancelEditName(); }}
                        className="bg-[#1f1f1f] text-white text-sm font-semibold rounded px-2 py-0.5 border border-blue-500 focus:outline-none w-full"
                        maxLength={100}
                        disabled={savingName}
                      />
                      <button onClick={handleSaveName} disabled={savingName} className="text-green-400 hover:text-green-500 flex-shrink-0 p-0.5"><Check size={14} /></button>
                      <button onClick={handleCancelEditName} disabled={savingName} className="text-red-400 hover:text-red-500 flex-shrink-0 p-0.5"><X size={14} /></button>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1.5 min-w-0">
                      <p className="text-white font-semibold text-sm truncate">{user?.name}</p>
                      <button onClick={handleStartEditName} className="text-gray-400 hover:text-white flex-shrink-0 p-0.5 rounded hover:bg-white/5 transition-colors"><Pencil size={12} /></button>
                    </div>
                  )}
                  {user?.email && <p className="text-gray-400 text-xs mt-0.5 truncate">{user.email}</p>}
                </div>
              </div>
              <nav className="flex flex-col gap-1">
                <Link href="/dashboard" onClick={() => setIsSidebarOpen(false)} className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors text-left text-gray-100 hover:bg-gray-800 ${activeSection === 'overview' ? 'bg-gray-800' : ''}`}>
                  <LayoutDashboard size={16} className="flex-shrink-0" /><span>Overview</span>
                </Link>
                <Link href="/contact" onClick={() => setIsSidebarOpen(false)} className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors text-left text-gray-100 hover:bg-gray-800 ${activeSection === 'contact' ? 'bg-gray-800' : ''}`}>
                  <Mail size={16} className="flex-shrink-0" /><span>Contact Us</span>
                </Link>
                <button onClick={() => setHistoryOpen(!historyOpen)} className="w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm text-gray-100 hover:bg-gray-800 transition-colors text-left">
                  <Clock size={16} className="flex-shrink-0" /><span className="flex-1">History</span>
                  <ChevronRight size={14} className={`flex-shrink-0 transition-transform ${historyOpen ? 'rotate-90' : ''}`} />
                </button>
                {historyOpen && (
                  <div className="ml-7 flex flex-col gap-0.5">
                    {analysisHistory.length === 0 ? (
                      <p className="text-xs text-gray-500 px-3 py-1">No history yet</p>
                    ) : (
                      <>
                        {analysisHistory.slice(0, historyVisibleCount).map((item) => (
                          <div key={item.id} className="relative group/item">
                            <button
                              onClick={() => handleSelectHistory(item.id)}
                              className={`block w-full text-left px-3 py-2 rounded transition-colors ${selectedHistoryId === item.id && pathname === '/history' ? 'bg-gray-800' : 'hover:bg-gray-800'}`}
                            >
                              <p className={`text-xs font-medium truncate pr-6 ${selectedHistoryId === item.id && pathname === '/history' ? 'text-gray-100' : 'text-gray-100'}`}>
                                {item.interestText}
                              </p>
                              <p className="text-[10px] text-gray-500 mt-0.5 font-normal">
                                {new Date(item.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                              </p>
                            </button>
                            <button
                              onClick={(e) => handleDeleteHistory(e, item.id)}
                              className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-500 hover:text-red-400 opacity-0 group-hover/item:opacity-100 transition-opacity"
                              title="Delete history"
                            >
                              <Trash2 size={16} />
                            </button>
                          </div>
                        ))}
                        <div className="flex items-center gap-2 mt-1">
                          {analysisHistory.length > historyVisibleCount && (
                            <button onClick={() => setHistoryVisibleCount(prev => prev + 5)} className="text-xs text-blue-400 hover:text-blue-300 px-3 py-1 transition-colors text-left flex-shrink-0">
                              View {Math.min(5, analysisHistory.length - historyVisibleCount)} more
                            </button>
                          )}
                          {historyVisibleCount > 5 && (
                            <button onClick={() => setHistoryVisibleCount(5)} className="text-xs text-gray-500 hover:text-gray-400 px-3 py-1 transition-colors text-left flex-shrink-0">
                              Show less
                            </button>
                          )}
                        </div>
                      </>
                    )}
                  </div>
                )}
                <button onClick={() => setChatHistoryOpen(!chatHistoryOpen)} className="w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm text-gray-100 hover:bg-gray-800 transition-colors text-left">
                  <MessageSquare size={16} className="flex-shrink-0" /><span className="flex-1">Chat History</span>
                  <ChevronRight size={14} className={`flex-shrink-0 transition-transform ${chatHistoryOpen ? 'rotate-90' : ''}`} />
                </button>
                {chatHistoryOpen && (
                  <div className="ml-7 flex flex-col gap-0.5">
                    {chatSessions.length === 0 ? (
                      <p className="text-xs text-gray-500 px-3 py-1">No chats yet</p>
                    ) : (
                      chatSessions.map((c, i) => (
                        <Link key={i} href={`/agent?sessionId=${c.id}`} onClick={() => setIsSidebarOpen(false)} className="block w-full text-left px-3 py-2 rounded transition-colors hover:bg-gray-800">
                          <p className="text-xs font-medium truncate pr-6 text-gray-100">
                            {c.title || `Chat ${i + 1}`}
                          </p>
                          <p className="text-[10px] text-gray-500 mt-0.5 font-normal">
                            {new Date(c.updatedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                          </p>
                        </Link>
                      ))
                    )}
                  </div>
                )}
              </nav>
            </div>
          </aside>
        </div>
      )}

      {/* Mobile FAB - bottom left, hidden on desktop */}
      <button
        onClick={() => setIsSidebarOpen(true)}
        className="md:hidden fixed bottom-6 left-6 z-[150] flex items-center justify-center w-12 h-12 rounded-full bg-gray-800 border border-gray-600 text-white shadow-lg hover:bg-gray-700 transition-colors"
        aria-label="Open sidebar"
      >
        <LayoutDashboard size={20} />
      </button>

      {/* Mobile Dashboard Sidebar Overlay */}
      {isSidebarOpen && (
        <div className="md:hidden fixed inset-0 z-[180]">
          <button className="absolute inset-0 bg-black/60 backdrop-blur-sm" aria-label="Close sidebar" onClick={() => setIsSidebarOpen(false)} />
          <aside className="absolute top-0 left-0 h-full w-72 max-w-[85%] bg-[#111111] border-r border-[#1f1f1f] overflow-y-auto shadow-2xl">
            <div className="p-7">
              <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-700">
                <div className="min-w-0 flex-1">
                  {isEditingName ? (
                    <div className="flex items-center gap-1">
                      <input
                        ref={editInputRefMobile}
                        value={editNameValue}
                        onChange={(e) => setEditNameValue(e.target.value)}
                        onKeyDown={(e) => { if (e.key === 'Enter') handleSaveName(); if (e.key === 'Escape') handleCancelEditName(); }}
                        className="bg-[#1f1f1f] text-white text-sm font-semibold rounded px-2 py-0.5 border border-blue-500 focus:outline-none w-full"
                        maxLength={100}
                        disabled={savingName}
                      />
                      <button onClick={handleSaveName} disabled={savingName} className="text-green-400 hover:text-green-500 flex-shrink-0 p-0.5"><Check size={14} /></button>
                      <button onClick={handleCancelEditName} disabled={savingName} className="text-red-400 hover:text-red-500 flex-shrink-0 p-0.5"><X size={14} /></button>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1.5 min-w-0">
                      <p className="text-white font-semibold text-sm truncate">{user?.name}</p>
                      <button onClick={handleStartEditName} className="text-gray-400 hover:text-white flex-shrink-0 p-0.5 rounded hover:bg-white/5 transition-colors"><Pencil size={12} /></button>
                    </div>
                  )}
                  {user?.email && <p className="text-gray-400 text-xs mt-0.5 truncate">{user.email}</p>}
                </div>
              </div>
              <nav className="flex flex-col gap-1">
                <Link href="/dashboard" onClick={() => setIsSidebarOpen(false)} className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors text-left text-gray-100 hover:bg-gray-800 ${activeSection === 'overview' ? 'bg-gray-800' : ''}`}>
                  <LayoutDashboard size={16} className="flex-shrink-0" /><span>Overview</span>
                </Link>
                <Link href="/contact" onClick={() => setIsSidebarOpen(false)} className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors text-left text-gray-100 hover:bg-gray-800 ${activeSection === 'contact' ? 'bg-gray-800' : ''}`}>
                  <Mail size={16} className="flex-shrink-0" /><span>Contact Us</span>
                </Link>
                <button onClick={() => setHistoryOpen(!historyOpen)} className="w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm text-gray-100 hover:bg-gray-800 transition-colors text-left">
                  <Clock size={16} className="flex-shrink-0" /><span className="flex-1">History</span>
                  <ChevronRight size={14} className={`flex-shrink-0 transition-transform ${historyOpen ? 'rotate-90' : ''}`} />
                </button>
                {historyOpen && (
                  <div className="ml-7 flex flex-col gap-0.5">
                    {analysisHistory.length === 0 ? (
                      <p className="text-xs text-gray-500 px-3 py-1">No history yet</p>
                    ) : (
                      <>
                        {analysisHistory.slice(0, historyVisibleCount).map((item) => (
                          <div key={item.id} className="relative group/item">
                            <button
                              onClick={() => handleSelectHistory(item.id)}
                              className={`block w-full text-left px-3 py-2 rounded transition-colors ${selectedHistoryId === item.id && pathname === '/history' ? 'bg-gray-800' : 'hover:bg-gray-800'}`}
                            >
                              <p className={`text-xs font-medium truncate pr-6 ${selectedHistoryId === item.id && pathname === '/history' ? 'text-gray-100' : 'text-gray-100'}`}>
                                {item.interestText}
                              </p>
                              <p className="text-[10px] text-gray-500 mt-0.5 font-normal">
                                {new Date(item.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                              </p>
                            </button>
                            <button
                              onClick={(e) => handleDeleteHistory(e, item.id)}
                              className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 text-gray-500 hover:text-red-400 opacity-0 group-hover/item:opacity-100 transition-opacity"
                              title="Delete history"
                            >
                              <Trash2 size={12} />
                            </button>
                          </div>
                        ))}
                        <div className="flex items-center gap-2 mt-1">
                          {analysisHistory.length > historyVisibleCount && (
                            <button onClick={() => setHistoryVisibleCount(prev => prev + 5)} className="text-xs text-blue-400 hover:text-blue-300 px-3 py-1 transition-colors text-left flex-shrink-0">
                              View {Math.min(5, analysisHistory.length - historyVisibleCount)} more
                            </button>
                          )}
                          {historyVisibleCount > 5 && (
                            <button onClick={() => setHistoryVisibleCount(5)} className="text-xs text-gray-500 hover:text-gray-400 px-3 py-1 transition-colors text-left flex-shrink-0">
                              Show less
                            </button>
                          )}
                        </div>
                      </>
                    )}
                  </div>
                )}
                <button onClick={() => setChatHistoryOpen(!chatHistoryOpen)} className="w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm text-gray-100 hover:bg-gray-800 transition-colors text-left">
                  <MessageSquare size={16} className="flex-shrink-0" /><span className="flex-1">Chat History</span>
                  <ChevronRight size={14} className={`flex-shrink-0 transition-transform ${chatHistoryOpen ? 'rotate-90' : ''}`} />
                </button>
                {chatHistoryOpen && (
                  <div className="ml-7 flex flex-col gap-0.5">
                    {chatSessions.length === 0 ? (
                      <p className="text-xs text-gray-500 px-3 py-1">No chats yet</p>
                    ) : (
                      chatSessions.map((c, i) => (
                        <Link key={i} href={`/agent?sessionId=${c.id}`} onClick={() => setIsSidebarOpen(false)} className="block w-full text-left px-3 py-2 rounded transition-colors hover:bg-gray-800">
                          <p className="text-xs font-medium truncate pr-6 text-gray-100">
                            {c.title || `Chat ${i + 1}`}
                          </p>
                          <p className="text-[10px] text-gray-500 mt-0.5 font-normal">
                            {new Date(c.updatedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                          </p>
                        </Link>
                      ))
                    )}
                  </div>
                )}
              </nav>
            </div>
          </aside>
        </div>
      )}
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
              <Link
                href="/dashboard"
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors text-left text-gray-100 hover:bg-gray-800 ${activeSection === 'overview' ? 'bg-gray-800' : ''}`}
              >
                <LayoutDashboard size={16} className="flex-shrink-0" />
                <span>Overview</span>
              </Link>

              {/* Contact Us */}
              <Link
                href="/contact"
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors text-left text-gray-100 hover:bg-gray-800 ${activeSection === 'contact' ? 'bg-gray-800' : ''}`}
              >
                <Mail size={16} className="flex-shrink-0" />
                <span>Contact Us</span>
              </Link>

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
                  {analysisHistory.length === 0 ? (
                    <p className="text-xs text-gray-500 px-3 py-1">No history yet</p>
                  ) : (
                    <>
                      {analysisHistory.slice(0, historyVisibleCount).map((item) => (
                        <div key={item.id} className="relative group/item">
                          <button
                            onClick={() => handleSelectHistory(item.id)}
                            className={`block w-full text-left px-3 py-2 rounded transition-colors ${selectedHistoryId === item.id && pathname === '/history' ? 'bg-gray-800' : 'hover:bg-gray-800'}`}
                          >
                            <p className="text-xs font-medium truncate pr-6 text-gray-100">
                              {item.interestText}
                            </p>
                            <p className="text-[10px] text-gray-500 mt-0.5 font-normal">
                              {new Date(item.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                            </p>
                          </button>
                          <button
                            onClick={(e) => handleDeleteHistory(e, item.id)}
                            className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-500 hover:text-red-400 opacity-0 group-hover/item:opacity-100 transition-opacity"
                            title="Delete history"
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>
                      ))}
                      <div className="flex items-center gap-2 mt-1">
                        {analysisHistory.length > historyVisibleCount && (
                          <button onClick={() => setHistoryVisibleCount(prev => prev + 5)} className="text-xs text-blue-400 hover:text-blue-300 px-3 py-1 transition-colors text-left flex-shrink-0">
                            View {Math.min(5, analysisHistory.length - historyVisibleCount)} more
                          </button>
                        )}
                        {historyVisibleCount > 5 && (
                          <button onClick={() => setHistoryVisibleCount(5)} className="text-xs text-gray-500 hover:text-gray-400 px-3 py-1 transition-colors text-left flex-shrink-0">
                            Show less
                          </button>
                        )}
                      </div>
                    </>
                  )}
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
                  {chatSessions.length === 0 ? (
                    <p className="text-xs text-gray-500 px-3 py-1">No chats yet</p>
                  ) : (
                    chatSessions.map((c, i) => (
                      <Link
                        key={i}
                        href={`/agent?sessionId=${c.id}`}
                        className="block w-full text-left px-3 py-2 rounded transition-colors hover:bg-gray-800"
                      >
                        <p className="text-xs font-medium truncate pr-6 text-gray-100">
                          {c.title || `Chat ${i + 1}`}
                        </p>
                        <p className="text-[10px] text-gray-500 mt-0.5 font-normal">
                          {new Date(c.updatedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                        </p>
                      </Link>
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
                <span className="text-sm text-gray-400">{activeSection === 'contact' ? 'Contact Us' : activeSection === 'history' ? 'Analysis History' : 'Dashboard'}</span>
              </div>
            </div>

            {/* Render Child Content Here with Context Provider */}
            <DashboardContext.Provider value={{
              analysisCount,
              chatCount,
              requestCount,
              recentAnalysis,
              statsLoading,
              analysisHistory,
              selectedHistoryId,
              setSelectedHistoryId
            }}>
              {children}
            </DashboardContext.Provider>

          </div>
        </main>
      </div>
    </div>
  );
}
