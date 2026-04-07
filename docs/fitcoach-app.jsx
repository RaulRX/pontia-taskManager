import React, { useState, useEffect, useRef } from 'react';
import { 
  Dumbbell, 
  Apple, 
  Calendar, 
  Settings, 
  MessageCircle, 
  User, 
  Home, 
  Plus, 
  Search, 
  Bell,
  Send,
  X,
  CheckCircle2,
  Zap, 
  ArrowLeft, 
  Activity, 
  Flame,
  ExternalLink,
  LogOut,
  ChevronRight,
  Shield,
  CreditCard,
  Sparkles,
  Smartphone,
  Globe,
  Lock,
  ChevronDown
} from 'lucide-react';

const App = () => {
  const [activeTab, setActiveTab] = useState('home');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDate, setSelectedDate] = useState(new Date(2024, 4, 10)); // Mayo 2024
  const [viewDetail, setViewDetail] = useState(null);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [messageInput, setMessageInput] = useState('');
  const [messages, setMessages] = useState([
    { id: 1, text: "¡Hola Alex! He revisado tu progreso de ayer. Vas muy bien con las cargas.", sender: "coach", time: "10:30 AM" },
    { id: 2, text: "¿Crees que deba aumentar el peso en la banca mañana?", sender: "user", time: "10:32 AM" },
    { id: 3, text: "Sí, sube 2.5kg por lado pero mantén las repeticiones en 10.", sender: "coach", time: "10:45 AM" }
  ]);

  const userMenuRef = useRef(null);

  // Cerrar menú de usuario al hacer click fuera
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setShowUserMenu(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Datos del Usuario
  const [user, setUser] = useState({
    name: "Alex García",
    email: "alex.garcia@email.com",
    goal: "Ganancia Muscular",
    plan: "Premium Fitness+",
    avatar: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=200&h=200&auto=format&fit=crop"
  });

  const [myPlans] = useState([
    { id: 1, title: "Rutina Hipertrofia A", type: "training", date: "2024-05-10", status: "En curso", progress: 65, color: "blue" },
    { id: 2, title: "Dieta Volumen Limpio", type: "nutrition", date: "2024-05-12", status: "Activo", progress: 40, color: "green" }
  ]);

  const scheduleData = {
    "2024-05-10": [
      { id: 1, title: "Pecho y Tríceps (Hipertrofia)", type: "training", time: "09:00 AM", color: "blue" },
      { id: 18, title: "Cena: Pollo con Batata", type: "nutrition", time: "21:00 PM", color: "green" }
    ],
    "2024-05-15": [
      { id: 20, title: "Sesión HIIT Cardio", type: "training", time: "07:30 AM", color: "red" },
      { id: 21, title: "Almuerzo: Ensalada Quinoa", type: "nutrition", time: "14:00 PM", color: "green" }
    ],
    "2024-05-22": [
      { id: 30, title: "Pierna y Core (Fuerza)", type: "training", time: "18:00 PM", color: "blue" }
    ]
  };

  const catalogPlans = [
    { id: 101, title: "Fuerza Explosiva", type: "training", level: "Avanzado", duration: "8 sem", rating: 4.8, category: "training" },
    { id: 102, title: "Ayuno Intermitente 16:8", type: "nutrition", level: "Intermedio", duration: "Indefinido", rating: 4.5, category: "nutrition" }
  ];

  const filteredCatalog = catalogPlans.filter(plan => {
    const matchesSearch = plan.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || plan.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!messageInput.trim()) return;
    const newMessage = {
      id: messages.length + 1,
      text: messageInput,
      sender: "user",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages([...messages, newMessage]);
    setMessageInput('');
  };

  // Helper para detalles
  const detailedPlans = {
    1: { id: 1, title: "Rutina Hipertrofia A", type: "training", description: "Enfoque en volumen.", image: "https://images.unsplash.com/photo-1583454110551-21f2fa2adfcd?q=80&w=800&auto=format&fit=crop", exercises: [{ name: "Press Banca", sets: "4x10", notes: "Lento" }] },
    2: { id: 2, title: "Dieta Volumen Limpio", type: "nutrition", description: "Superávit controlado.", image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=800&auto=format&fit=crop", foods: [{ name: "Pollo", cal: 330 }], totalCalories: 1000 }
  };

  if (viewDetail) {
    const detail = detailedPlans[viewDetail];
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col animate-in fade-in duration-300">
        <header className="p-4 bg-white border-b flex items-center gap-4 sticky top-0 z-50">
          <button onClick={() => setViewDetail(null)} className="p-2 hover:bg-slate-100 rounded-full transition-colors"><ArrowLeft size={24} /></button>
          <h2 className="font-bold text-lg">Detalles del Plan</h2>
        </header>
        <main className="max-w-3xl mx-auto w-full p-4 md:p-8 space-y-6">
          <div className="rounded-3xl overflow-hidden shadow-sm border bg-white">
            <img src={detail.image} className="w-full h-64 object-cover" />
            <div className="p-6">
               <h1 className="text-3xl font-bold mb-4">{detail.title}</h1>
               <p className="text-slate-600 mb-6">{detail.description}</p>
               {detail.type === 'training' ? (
                 detail.exercises.map((ex, i) => <div key={i} className="p-4 bg-slate-50 rounded-2xl mb-2 flex justify-between"><span>{ex.name}</span><b>{ex.sets}</b></div>)
               ) : (
                 detail.foods.map((f, i) => <div key={i} className="p-4 bg-slate-50 rounded-2xl mb-2 flex justify-between"><span>{f.name}</span><b>{f.cal} kcal</b></div>)
               )}
            </div>
          </div>
          <button onClick={() => setViewDetail(null)} className="w-full py-4 bg-indigo-600 text-white font-bold rounded-2xl">Volver</button>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans pb-20 md:pb-0 md:pl-64 flex">
      
      {/* SIDEBAR DESKTOP */}
      <nav className="hidden md:flex fixed left-0 top-0 h-full w-64 bg-white border-r border-slate-200 flex-col p-6 z-40">
        <div className="flex items-center gap-3 mb-10">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-100">
            <Activity size={24} />
          </div>
          <span className="text-xl font-bold tracking-tight">FitnessHub</span>
        </div>

        <div className="space-y-1 flex-1">
          <NavItem active={activeTab === 'home'} onClick={() => setActiveTab('home')} icon={<Home size={20}/>} label="Mi Panel" />
          <NavItem active={activeTab === 'calendar'} onClick={() => setActiveTab('calendar')} icon={<Calendar size={20}/>} label="Calendario" />
          <NavItem active={activeTab === 'explore'} onClick={() => setActiveTab('explore')} icon={<Search size={20}/>} label="Explorar Planes" />
          <NavItem active={activeTab === 'messages'} onClick={() => setActiveTab('messages')} icon={<MessageCircle size={20}/>} label="Mensajes" />
          <NavItem active={activeTab === 'settings' || activeTab === 'profile'} onClick={() => setActiveTab('profile')} icon={<Settings size={20}/>} label="Ajustes" />
        </div>

        <div className="pt-6 border-t relative" ref={userMenuRef}>
          {showUserMenu && (
            <div className="absolute bottom-full left-0 w-full mb-2 bg-white rounded-2xl shadow-xl border border-slate-100 p-2 animate-in slide-in-from-bottom-2 duration-200 z-50">
              <button onClick={() => {setActiveTab('profile'); setShowUserMenu(false)}} className="w-full flex items-center gap-3 p-3 hover:bg-slate-50 rounded-xl text-sm font-semibold transition-colors">
                <User size={16} className="text-slate-400" /> Mi Perfil
              </button>
              <button className="w-full flex items-center gap-3 p-3 hover:bg-slate-50 rounded-xl text-sm font-semibold transition-colors">
                <CreditCard size={16} className="text-slate-400" /> Facturación
              </button>
              <button className="w-full flex items-center gap-3 p-3 hover:bg-slate-50 rounded-xl text-sm font-semibold transition-colors">
                <Shield size={16} className="text-slate-400" /> Privacidad
              </button>
              <div className="h-px bg-slate-100 my-1"></div>
              <button className="w-full flex items-center gap-3 p-3 hover:bg-red-50 text-red-600 rounded-xl text-sm font-semibold transition-colors">
                <LogOut size={16} /> Cerrar Sesión
              </button>
            </div>
          )}
          <div 
            onClick={() => setShowUserMenu(!showUserMenu)}
            className={`flex items-center gap-3 p-2 hover:bg-slate-50 rounded-xl cursor-pointer transition-colors ${showUserMenu ? 'bg-slate-50' : ''}`}
          >
            <img src={user.avatar} className="w-10 h-10 rounded-full object-cover border-2 border-indigo-100" />
            <div className="overflow-hidden">
              <p className="text-sm font-semibold truncate">{user.name}</p>
              <p className="text-xs text-slate-500 truncate">Plan Premium</p>
            </div>
          </div>
        </div>
      </nav>

      {/* CONTENIDO PRINCIPAL */}
      <div className="flex-1 overflow-y-auto">
        <header className="md:hidden flex items-center justify-between p-4 bg-white border-b sticky top-0 z-30">
          <span className="text-xl font-bold text-indigo-600 flex items-center gap-2"><Activity size={20} /> FitnessHub</span>
          <div className="flex items-center gap-4">
            <Bell size={20} className="text-slate-400" />
            <img src={user.avatar} onClick={() => setActiveTab('profile')} className="w-8 h-8 rounded-full object-cover" />
          </div>
        </header>

        <main className="max-w-5xl mx-auto p-4 md:p-10">
          
          {activeTab === 'home' && (
            <div className="space-y-8 animate-in fade-in duration-500">
              <section className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <h1 className="text-3xl font-bold text-slate-900">Bienvenido, {user.name.split(' ')[0]}</h1>
                  <p className="text-slate-500 mt-1">Tu progreso hoy va por buen camino.</p>
                </div>
                <div className="bg-white p-2 rounded-lg border flex items-center gap-2 px-4 shadow-sm h-fit w-fit">
                  <Zap size={16} className="text-amber-500 fill-amber-500" />
                  <span className="text-sm font-bold">Racha: 12 días</span>
                </div>
              </section>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {myPlans.map(plan => (
                  <PlanCard key={plan.id} plan={plan} onClick={() => setViewDetail(plan.id)} />
                ))}
                <button onClick={() => setActiveTab('explore')} className="border-2 border-dashed border-slate-200 rounded-3xl flex flex-col items-center justify-center p-8 text-slate-400 hover:border-indigo-300 hover:text-indigo-500 hover:bg-indigo-50/30 transition-all group">
                  <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mb-3 group-hover:bg-indigo-100 transition-colors"><Plus size={24} /></div>
                  <span className="font-semibold">Nuevo Plan</span>
                </button>
              </div>

              <section className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="font-bold text-xl">Eventos para el 10 Mayo</h2>
                  <button onClick={() => setActiveTab('calendar')} className="text-indigo-600 text-sm font-semibold hover:underline">Ver agenda completa</button>
                </div>
                <div className="space-y-4">
                  {scheduleData["2024-05-10"].map(event => (
                    <ScheduleItem key={event.id} time={event.time} title={event.title} category={event.type === 'training' ? 'Entrenamiento' : 'Nutrición'} active={event.type === 'training'} />
                  ))}
                </div>
              </section>
            </div>
          )}

          {activeTab === 'calendar' && (
            <div className="space-y-6 animate-in zoom-in-95 duration-300">
               <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  <div className="lg:col-span-2 bg-white rounded-3xl p-6 shadow-sm border border-slate-100">
                    <CalendarGrid selectedDate={selectedDate} onDateSelect={(date) => setSelectedDate(date)} data={scheduleData} />
                  </div>
                  <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 h-fit">
                    <h3 className="font-bold text-lg mb-6 flex items-center justify-between">Actividades <span className="text-xs text-slate-400">{selectedDate.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })}</span></h3>
                    <div className="space-y-4">
                      {(scheduleData[selectedDate.toISOString().split('T')[0]] || []).map(event => (
                        <ScheduleItem key={event.id} time={event.time} title={event.title} category={event.type === 'training' ? 'Entrenamiento' : 'Nutrición'} />
                      ))}
                    </div>
                  </div>
               </div>
            </div>
          )}

          {activeTab === 'messages' && (
            <div className="h-[calc(100vh-200px)] md:h-[calc(100vh-80px)] bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden flex animate-in slide-in-from-bottom-4 duration-500">
              <div className="w-20 md:w-72 border-r bg-slate-50/50 flex flex-col">
                <div className="p-4 md:p-6 border-b bg-white">
                  <h2 className="hidden md:block font-bold text-xl">Mensajes</h2>
                  <div className="md:hidden flex justify-center"><MessageCircle className="text-indigo-600" /></div>
                </div>
                <div className="flex-1 overflow-y-auto">
                  <div className="p-2 md:p-3 bg-indigo-50 border-r-4 border-indigo-600 flex items-center gap-3">
                    <div className="w-10 h-10 bg-indigo-100 rounded-full flex-shrink-0 flex items-center justify-center text-indigo-600 font-bold">C</div>
                    <div className="hidden md:block overflow-hidden">
                      <p className="text-sm font-bold truncate">Tu Entrenador</p>
                      <p className="text-xs text-indigo-600 font-medium truncate">En línea</p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex-1 flex flex-col bg-white">
                <div className="p-4 border-b flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold text-xs">C</div>
                    <p className="font-bold text-slate-800">Tu Entrenador</p>
                  </div>
                </div>
                <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-slate-50/30">
                  {messages.map(msg => (
                    <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[80%] p-4 rounded-2xl text-sm shadow-sm ${msg.sender === 'user' ? 'bg-indigo-600 text-white rounded-br-none' : 'bg-white text-slate-700 border border-slate-100 rounded-bl-none'}`}>
                        {msg.text}
                        <p className={`text-[10px] mt-1 ${msg.sender === 'user' ? 'text-indigo-100' : 'text-slate-400'}`}>{msg.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <form onSubmit={handleSendMessage} className="p-4 border-t flex gap-3">
                  <input 
                    type="text" 
                    value={messageInput}
                    onChange={(e) => setMessageInput(e.target.value)}
                    placeholder="Escribe un mensaje..." 
                    className="flex-1 bg-slate-100 border-none rounded-2xl px-5 py-3 text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                  />
                  <button type="submit" className="bg-indigo-600 text-white p-3 rounded-2xl hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-100">
                    <Send size={20} />
                  </button>
                </form>
              </div>
            </div>
          )}

          {activeTab === 'explore' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 animate-in slide-in-from-right-4 duration-500">
              {filteredCatalog.map(item => <CatalogItem key={item.id} item={item} />)}
            </div>
          )}

          {activeTab === 'profile' && (
            <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-500 pb-10">
              {/* Header de Perfil */}
              <div className="bg-white rounded-[2rem] shadow-sm border p-8 flex flex-col md:flex-row items-center gap-8 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-6 opacity-5">
                   <Activity size={120} />
                </div>
                <div className="relative">
                  <img src={user.avatar} className="w-32 h-32 rounded-full object-cover border-4 border-indigo-50 shadow-xl" />
                  <button className="absolute bottom-0 right-0 bg-white p-2 rounded-full shadow-md border hover:bg-slate-50 transition-colors">
                    <Plus size={16} className="text-indigo-600" />
                  </button>
                </div>
                <div className="text-center md:text-left flex-1">
                  <div className="flex flex-col md:flex-row md:items-center gap-2 md:gap-4 mb-2">
                    <h2 className="text-3xl font-black text-slate-800">{user.name}</h2>
                    <span className="bg-indigo-600 text-white px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider flex items-center gap-1 w-fit mx-auto md:mx-0">
                      <Sparkles size={12} /> {user.plan}
                    </span>
                  </div>
                  <p className="text-slate-500 font-medium mb-4">{user.email}</p>
                  <div className="flex flex-wrap justify-center md:justify-start gap-3">
                    <div className="bg-slate-50 px-4 py-2 rounded-xl border border-slate-100 text-xs font-bold text-slate-600 flex items-center gap-2">
                      <Flame size={14} className="text-orange-500" /> Meta: {user.goal}
                    </div>
                    <div className="bg-slate-50 px-4 py-2 rounded-xl border border-slate-100 text-xs font-bold text-slate-600 flex items-center gap-2">
                      <Zap size={14} className="text-amber-500" /> Racha: 12 días
                    </div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Lo que incluye el plan */}
                <div className="bg-white rounded-[2rem] shadow-sm border p-8 flex flex-col">
                  <h3 className="font-black text-lg mb-6 flex items-center gap-2">
                    <CreditCard size={20} className="text-indigo-600" /> Detalles del Plan
                  </h3>
                  <div className="space-y-4 flex-1">
                    {[
                      "Acceso ilimitado a rutinas IA",
                      "Soporte 24/7 con tu entrenador",
                      "Planes nutricionales personalizados",
                      "Análisis biométrico semanal",
                      "Acceso a webinars exclusivos"
                    ].map((item, i) => (
                      <div key={i} className="flex items-center gap-3">
                        <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                          <CheckCircle2 size={12} />
                        </div>
                        <span className="text-sm font-semibold text-slate-600">{item}</span>
                      </div>
                    ))}
                  </div>
                  <button className="w-full mt-8 py-3 bg-slate-50 text-slate-600 rounded-2xl font-bold text-sm hover:bg-slate-100 transition-colors border border-slate-200">
                    Gestionar Suscripción
                  </button>
                </div>

                {/* Perfil generado por IA */}
                <div className="bg-indigo-900 rounded-[2rem] shadow-xl p-8 text-white flex flex-col relative overflow-hidden group">
                  <div className="absolute -top-10 -right-10 opacity-10 group-hover:scale-110 transition-transform duration-500">
                     <Sparkles size={200} />
                  </div>
                  <h3 className="font-black text-lg mb-4 flex items-center gap-2">
                    <Sparkles size={20} className="text-amber-400" /> Perfil Bio-Inteligente
                  </h3>
                  <p className="text-indigo-200 text-sm mb-6 leading-relaxed">
                    Nuestra IA ha analizado tus 3 meses de progreso. Tienes un perfil tipo <b>"Endo-Mesomorfo"</b> con alta capacidad de recuperación.
                  </p>
                  <div className="space-y-3 mb-8">
                    <div className="bg-white/10 p-4 rounded-2xl backdrop-blur-sm border border-white/5">
                      <p className="text-[10px] uppercase font-bold text-indigo-300 mb-1">Potencial Muscular</p>
                      <div className="w-full bg-white/20 h-1.5 rounded-full">
                        <div className="bg-amber-400 h-full rounded-full w-[85%]"></div>
                      </div>
                    </div>
                  </div>
                  <button className="w-full py-4 bg-white text-indigo-900 rounded-2xl font-black text-sm hover:bg-indigo-50 transition-all flex items-center justify-center gap-2">
                    Ver Informe Completo IA <ChevronRight size={16} />
                  </button>
                </div>
              </div>

              {/* Ajustes de la aplicación */}
              <div className="bg-white rounded-[2rem] shadow-sm border p-8">
                <h3 className="font-black text-lg mb-6 flex items-center gap-2">
                  <Settings size={20} className="text-indigo-600" /> Ajustes de Aplicación
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
                  <SettingsToggle label="Notificaciones Push" icon={<Bell size={18}/>} active />
                  <SettingsToggle label="Modo Oscuro Automático" icon={<Smartphone size={18}/>} />
                  <SettingsToggle label="Sincronizar Salud (Apple/Google)" icon={<Activity size={18}/>} active />
                  <SettingsToggle label="Idioma" value="Español (ES)" icon={<Globe size={18}/>} />
                  <SettingsToggle label="Autenticación Biométrica" icon={<Lock size={18}/>} active />
                </div>
              </div>
            </div>
          )}

          {(activeTab === 'settings' && activeTab !== 'profile') && (
            <div className="max-w-2xl mx-auto space-y-8 animate-in fade-in duration-500">
               <div className="bg-white rounded-3xl shadow-sm border p-8 space-y-8">
                  <div className="flex flex-col items-center text-center space-y-4">
                    <img src={user.avatar} className="w-32 h-32 rounded-full object-cover border-4 border-indigo-50 shadow-xl" />
                    <h2 className="text-2xl font-bold">{user.name}</h2>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <InputField label="Nombre Completo" value={user.name} />
                    <InputField label="Email Personal" value={user.email} />
                  </div>
               </div>
            </div>
          )}
        </main>
      </div>

      <footer className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t flex justify-around p-3 z-40 shadow-lg">
        <NavIcon active={activeTab === 'home'} icon={<Home />} label="Inicio" onClick={() => setActiveTab('home')} />
        <NavIcon active={activeTab === 'calendar'} icon={<Calendar />} label="Agenda" onClick={() => setActiveTab('calendar')} />
        <NavIcon active={activeTab === 'messages'} icon={<MessageCircle />} label="Chat" onClick={() => setActiveTab('messages')} />
        <NavIcon active={activeTab === 'profile'} icon={<User />} label="Perfil" onClick={() => setActiveTab('profile')} />
      </footer>
    </div>
  );
};

// COMPONENTES AUXILIARES

const SettingsToggle = ({ label, icon, active = false, value = null }) => (
  <div className="flex items-center justify-between py-4 border-b border-slate-50 last:border-0 group">
    <div className="flex items-center gap-3">
      <div className="text-slate-400 group-hover:text-indigo-600 transition-colors">{icon}</div>
      <span className="text-sm font-bold text-slate-700">{label}</span>
    </div>
    {value ? (
      <div className="flex items-center gap-1 text-xs font-black text-indigo-600 bg-indigo-50 px-3 py-1.5 rounded-lg cursor-pointer">
        {value} <ChevronDown size={14} />
      </div>
    ) : (
      <div className={`w-11 h-6 rounded-full p-1 transition-colors cursor-pointer ${active ? 'bg-indigo-600' : 'bg-slate-200'}`}>
        <div className={`bg-white w-4 h-4 rounded-full shadow-sm transition-transform ${active ? 'translate-x-5' : 'translate-x-0'}`}></div>
      </div>
    )}
  </div>
);

const NavItem = ({ active, icon, label, onClick }) => (
  <button onClick={onClick} className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-2xl font-bold transition-all duration-300 ${active ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600'}`}>
    {icon} <span className="text-sm">{label}</span>
  </button>
);

const NavIcon = ({ active, icon, label, onClick }) => (
  <button onClick={onClick} className={`flex flex-col items-center gap-1 p-2 transition-all ${active ? 'text-indigo-600 scale-110' : 'text-slate-400'}`}>
    {React.cloneElement(icon, { size: 24 })}
    <span className="text-[9px] font-black uppercase tracking-widest">{label}</span>
  </button>
);

const PlanCard = ({ plan, onClick }) => (
  <div onClick={onClick} className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm cursor-pointer relative overflow-hidden transition-all duration-300 transform hover:-translate-y-2 hover:shadow-xl hover:border-indigo-200 group">
    <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity"><ExternalLink size={16} className="text-indigo-400" /></div>
    <div className={`w-12 h-12 rounded-2xl bg-${plan.color}-50 flex items-center justify-center text-${plan.color}-600 mb-4 group-hover:scale-110 transition-transform`}>
      {plan.type === 'training' ? <Dumbbell size={24} /> : <Apple size={24} />}
    </div>
    <h3 className="font-bold text-slate-800 mb-1 group-hover:text-indigo-600 transition-colors">{plan.title}</h3>
    <div className="w-full bg-slate-100 h-2 rounded-full mt-4 overflow-hidden">
      <div className={`bg-${plan.color}-500 h-full`} style={{ width: `${plan.progress}%` }}></div>
    </div>
    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-3">{plan.progress}% COMPLETADO</p>
  </div>
);

const ScheduleItem = ({ time, title, category, active = false }) => (
  <div className={`flex items-start gap-4 p-4 rounded-2xl transition-all border ${active ? 'bg-indigo-50 border-indigo-100' : 'bg-white border-transparent hover:bg-slate-50'}`}>
    <span className="text-xs font-black text-slate-400 min-w-[70px] pt-1">{time}</span>
    <div className="flex-1">
      <h4 className={`font-bold text-sm ${active ? 'text-indigo-900' : 'text-slate-800'}`}>{title}</h4>
      <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">{category}</p>
    </div>
    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${active ? 'border-indigo-600 bg-white text-indigo-600' : 'border-slate-200 text-transparent'}`}>
      <CheckCircle2 size={14} />
    </div>
  </div>
);

const CatalogItem = ({ item }) => (
  <div className="bg-white rounded-3xl border border-slate-100 overflow-hidden hover:shadow-xl transition-all group">
    <div className="h-32 bg-slate-200 relative overflow-hidden">
      <img src="https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=400&h=250&auto=format&fit=crop" className="w-full h-full object-cover group-hover:scale-110 transition-transform" />
      <div className="absolute inset-0 bg-black/20"></div>
      <div className="absolute bottom-3 left-4 text-white z-10"><p className="text-[9px] font-black uppercase">{item.level}</p><h4 className="font-bold text-sm">{item.title}</h4></div>
    </div>
    <div className="p-4"><button className="w-full py-2.5 bg-indigo-600 text-white rounded-xl font-bold text-xs hover:bg-indigo-700">Activar Plan</button></div>
  </div>
);

const CalendarGrid = ({ selectedDate, onDateSelect, data }) => {
  const currentMonth = new Date(2024, 4, 1);
  const days = [];
  const startDay = new Date(2024, 4, 1).getDay();
  const offset = startDay === 0 ? 6 : startDay - 1;
  for (let i = 0; i < offset; i++) days.push(null);
  for (let d = 1; d <= 31; d++) days.push(new Date(2024, 4, d));

  return (
    <div className="select-none">
      <h2 className="font-black text-2xl capitalize mb-8 text-slate-800">Mayo 2024</h2>
      <div className="grid grid-cols-7 gap-2 mb-4 text-center">
        {['Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'Do'].map(day => <span key={day} className="text-[10px] font-black text-slate-400 uppercase">{day}</span>)}
      </div>
      <div className="grid grid-cols-7 gap-2">
        {days.map((day, idx) => {
          if (!day) return <div key={idx} className="aspect-square"></div>;
          const isSelected = day.toDateString() === selectedDate.toDateString();
          const dateKey = day.toISOString().split('T')[0];
          return (
            <div key={idx} onClick={() => onDateSelect(day)} className={`aspect-square flex flex-col items-center justify-center rounded-2xl cursor-pointer border-2 transition-all ${isSelected ? 'bg-indigo-600 border-indigo-600 text-white shadow-lg' : 'bg-white border-slate-50 hover:border-indigo-100'}`}>
              <span className="text-sm font-bold">{day.getDate()}</span>
              {data[dateKey] && <div className="flex gap-0.5 mt-1">{data[dateKey].map((_, i) => <div key={i} className={`w-1 h-1 rounded-full ${isSelected ? 'bg-white' : 'bg-indigo-500'}`}></div>)}</div>}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const InputField = ({ label, value }) => (
  <div className="space-y-1.5">
    <label className="text-[10px] font-black text-slate-400 uppercase">{label}</label>
    <input type="text" defaultValue={value} className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm font-semibold outline-none" />
  </div>
);

export default App;