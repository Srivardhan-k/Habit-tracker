import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  Target, 
  BarChart2, 
  Bot, 
  Settings, 
  Crown, 
  Menu, 
  X,
  Info
} from 'lucide-react';
import HabitList from './components/HabitList';
import Analytics from './components/Analytics';
import AICoach from './components/AICoach';
import VisionBoard from './components/VisionBoard';
import { Habit } from './types';

// Mock Premium feature handler
const PremiumModal = ({ onClose, onUpgrade }: { onClose: () => void, onUpgrade: () => void }) => (
  <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div className="bg-white rounded-2xl max-w-md w-full p-8 text-center shadow-2xl relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-yellow-400 to-orange-500"></div>
      <Crown className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
      <h2 className="text-2xl font-bold text-slate-900 mb-2">Upgrade to Orbit Pro</h2>
      <p className="text-slate-500 mb-6">Unlock the full power of Gemini AI to supercharge your productivity.</p>
      
      <div className="text-left space-y-3 mb-8 bg-slate-50 p-4 rounded-xl">
        <div className="flex items-center gap-3">
            <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center text-green-600">✓</div>
            <span className="text-sm">Unlimited Habits</span>
        </div>
        <div className="flex items-center gap-3">
            <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center text-green-600">✓</div>
            <span className="text-sm">4K Vision Board Generation (Nano Banana Pro)</span>
        </div>
        <div className="flex items-center gap-3">
            <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center text-green-600">✓</div>
            <span className="text-sm">Unlimited AI Coach Chat (Gemini 3 Pro)</span>
        </div>
      </div>

      <button 
        onClick={onUpgrade}
        className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold py-3 rounded-xl hover:shadow-lg hover:scale-[1.02] transition-all"
      >
        Start 7-Day Free Trial
      </button>
      <button onClick={onClose} className="mt-4 text-sm text-slate-400 hover:text-slate-600">Maybe Later</button>
    </div>
  </div>
);

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'habits' | 'analytics' | 'coach' | 'vision'>('habits');
  const [habits, setHabits] = useState<Habit[]>([]);
  const [isPremium, setIsPremium] = useState(false);
  const [showPremiumModal, setShowPremiumModal] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const [showInfo, setShowInfo] = useState(false);

  const handleUpgrade = () => {
    setIsPremium(true);
    setShowPremiumModal(false);
  };

  const NavItem = ({ id, icon: Icon, label }: { id: typeof activeTab, icon: any, label: string }) => (
    <button
      onClick={() => {
        setActiveTab(id);
        setShowMobileMenu(false);
      }}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
        activeTab === id 
          ? 'bg-indigo-600 text-white shadow-md' 
          : 'text-slate-500 hover:bg-slate-100'
      }`}
    >
      <Icon size={20} />
      <span className="font-medium">{label}</span>
    </button>
  );

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Mobile Header */}
      <div className="lg:hidden fixed top-0 w-full bg-white border-b border-slate-200 z-30 px-4 py-3 flex justify-between items-center">
        <div className="flex items-center gap-2 font-bold text-xl text-slate-800">
           <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white">O</div>
           Orbit
        </div>
        <button onClick={() => setShowMobileMenu(!showMobileMenu)}>
            {showMobileMenu ? <X /> : <Menu />}
        </button>
      </div>

      {/* Sidebar */}
      <aside className={`
        fixed inset-y-0 left-0 z-40 w-64 bg-white border-r border-slate-200 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static
        ${showMobileMenu ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="p-6 h-full flex flex-col">
          <div className="flex items-center gap-2 font-bold text-2xl text-slate-800 mb-8 px-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white">O</div>
            Orbit
          </div>

          <div className="space-y-2 flex-1">
            <NavItem id="habits" icon={LayoutDashboard} label="Habits" />
            <NavItem id="analytics" icon={BarChart2} label="Analytics" />
            <NavItem id="coach" icon={Bot} label="AI Coach" />
            <NavItem id="vision" icon={Target} label="Vision Board" />
          </div>

          <div className="mt-auto pt-6 border-t border-slate-100 space-y-3">
             {!isPremium && (
                 <button 
                  onClick={() => setShowPremiumModal(true)}
                  className="w-full bg-gradient-to-r from-orange-100 to-yellow-100 text-orange-700 p-3 rounded-xl flex items-center gap-3 hover:shadow-sm transition-all"
                 >
                    <Crown size={20} className="text-orange-500" />
                    <div className="text-left">
                        <p className="text-xs font-bold uppercase tracking-wider">Upgrade</p>
                        <p className="text-sm font-semibold">Get Pro Features</p>
                    </div>
                 </button>
             )}
             <button onClick={() => setShowInfo(true)} className="flex items-center gap-3 px-4 py-2 text-slate-400 hover:text-slate-600 text-sm">
                <Info size={16} /> About & Strategy
             </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto w-full pt-16 lg:pt-0">
        <div className="max-w-5xl mx-auto p-4 lg:p-8">
            {activeTab === 'habits' && <HabitList habits={habits} setHabits={setHabits} isPremium={isPremium} />}
            {activeTab === 'analytics' && <Analytics habits={habits} />}
            {activeTab === 'coach' && <AICoach isPremium={isPremium} onUpgrade={() => setShowPremiumModal(true)} />}
            {activeTab === 'vision' && <VisionBoard isPremium={isPremium} onUpgrade={() => setShowPremiumModal(true)} />}
        </div>
      </main>

      {/* Modals */}
      {showPremiumModal && <PremiumModal onClose={() => setShowPremiumModal(false)} onUpgrade={handleUpgrade} />}
      
      {showInfo && (
          <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
              <div className="bg-white rounded-xl p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto">
                  <div className="flex justify-between items-center mb-4">
                      <h2 className="text-xl font-bold">Orbit Strategy & Details</h2>
                      <button onClick={() => setShowInfo(false)}><X size={20}/></button>
                  </div>
                  <div className="prose prose-sm prose-slate">
                      <h3>Monetization Strategy</h3>
                      <ul>
                          <li><strong>Freemium Model:</strong> Core habit tracking is free (up to 5 habits). This builds daily retention.</li>
                          <li><strong>Premium Hooks:</strong> 
                              <ul className="list-disc pl-4 mt-1">
                                  <li><strong>AI Vision Board:</strong> High-res (2K/4K) generation locked behind Pro. Uses Gemini 3 Pro.</li>
                                  <li><strong>Deep Coaching:</strong> Unlimited chat with the Coach (Gemini 3 Pro) is Premium. Free users get 3 msgs/session.</li>
                              </ul>
                          </li>
                      </ul>
                      <h3>Play Store Deployment</h3>
                      <ul>
                          <li><strong>PWA/TWA:</strong> This React app is PWA-ready. Wrap in a Trusted Web Activity (TWA) container for Play Store.</li>
                          <li><strong>Privacy:</strong> Requires Camera/Gallery permissions for Vision Board upgrades (future feature).</li>
                          <li><strong>Store Assets:</strong> Focus screenshots on the "Vision Board" and "AI Coach" as differentiators.</li>
                      </ul>
                      <h3>Technical Stack</h3>
                      <ul>
                          <li>React 18, TypeScript, Tailwind CSS.</li>
                          <li><strong>Gemini 2.5 Flash Lite:</strong> For fast habit suggestions.</li>
                          <li><strong>Gemini 3 Pro:</strong> For complex coaching logic.</li>
                          <li><strong>Gemini 3 Pro Image (Nano Banana Pro):</strong> For Vision Board generation.</li>
                          <li><strong>Gemini 2.5 Flash Image:</strong> For editing vision board images.</li>
                      </ul>
                  </div>
              </div>
          </div>
      )}
    </div>
  );
};

export default App;
