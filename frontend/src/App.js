import React, { useState, useEffect } from 'react';
import { AlertCircle, User, CreditCard, ArrowUpRight, ArrowDownLeft, Plus, Eye, EyeOff, LogOut, Activity } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

const UniBank = () => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [currentView, setCurrentView] = useState('dashboard');
  const [accounts, setAccounts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Forms state
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ email: '', full_name: '', password: '', role: 'user' });
  const [transactionForm, setTransactionForm] = useState({ amount: '', receiver_account_id: '', sender_account_id: '' });

  useEffect(() => {
    if (token) {
      fetchUserData();
    }
  }, [token]);

  const apiCall = async (endpoint, method = 'GET', data = null) => {
    try {
      const config = {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        },
        ...(data && { body: JSON.stringify(data) })
      };

      const response = await fetch(`${API_BASE}${endpoint}`, config);
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || 'Error en la petición');
      }

      return result;
    } catch (error) {
      setMessage(`Error: ${error.message}`);
      throw error;
    }
  };

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const accountsData = await apiCall('/accounts');
      setAccounts(accountsData);
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('username', loginForm.email);
      formData.append('password', loginForm.password);

      const response = await fetch(`${API_BASE}/auth/token`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        setToken(data.access_token);
        localStorage.setItem('token', data.access_token);
        setMessage('¡Login exitoso!');
        setLoginForm({ email: '', password: '' });
      } else {
        setMessage(`Error: ${data.detail}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    try {
      setLoading(true);
      await apiCall('/auth/register', 'POST', registerForm);
      setMessage('¡Usuario registrado exitosamente! Ahora puedes hacer login.');
      setRegisterForm({ email: '', full_name: '', password: '', role: 'user' });
    } catch (error) {
      console.error('Error registering:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    setAccounts([]);
    setCurrentView('dashboard');
    localStorage.removeItem('token');
    setMessage('¡Sesión cerrada!');
  };

  const createAccount = async () => {
    try {
      setLoading(true);
      await apiCall('/accounts', 'POST');
      setMessage('¡Cuenta creada exitosamente!');
      fetchUserData();
    } catch (error) {
      console.error('Error creating account:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTransaction = async () => {
    try {
      setLoading(true);
      const url = `/transactions?sender_account_id=${transactionForm.sender_account_id}`;
      await apiCall(url, 'POST', {
        amount: parseFloat(transactionForm.amount),
        receiver_account_id: parseInt(transactionForm.receiver_account_id)
      });
      setMessage('¡Transferencia realizada exitosamente!');
      setTransactionForm({ amount: '', receiver_account_id: '', sender_account_id: '' });
      fetchUserData();
    } catch (error) {
      console.error('Error in transaction:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeposit = async () => {
    try {
      setLoading(true);
      await apiCall('/transactions/deposit', 'POST', {
        amount: parseFloat(transactionForm.amount),
        receiver_account_id: parseInt(transactionForm.receiver_account_id)
      });
      setMessage('¡Depósito realizado exitosamente!');
      setTransactionForm({ amount: '', receiver_account_id: '', sender_account_id: '' });
      fetchUserData();
    } catch (error) {
      console.error('Error in deposit:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleWithdraw = async () => {
    try {
      setLoading(true);
      await apiCall('/transactions/withdraw', 'POST', {
        amount: parseFloat(transactionForm.amount),
        sender_account_id: parseInt(transactionForm.sender_account_id)
      });
      setMessage('¡Retiro realizado exitosamente!');
      setTransactionForm({ amount: '', receiver_account_id: '', sender_account_id: '' });
      fetchUserData();
    } catch (error) {
      console.error('Error in withdrawal:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTransactions = async (accountId) => {
    try {
      setLoading(true);
      const data = await apiCall(`/transactions/${accountId}`);
      setTransactions(data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const data = await apiCall('/access-logs');
      setLogs(data);
    } catch (error) {
      console.error('Error fetching logs:', error);
    } finally {
      setLoading(false);
    }
  };

  // Render different views
  const renderAuthForms = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">🏦 UniBank</h1>
          <p className="text-gray-600">Sistema Bancario con AOP</p>
        </div>

        <div className="space-y-6">
          {/* Login Form */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Iniciar Sesión</h2>
            <div className="space-y-4">
              <input
                type="email"
                placeholder="Email"
                value={loginForm.email}
                onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="password"
                placeholder="Contraseña"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              />
              <button
                onClick={handleLogin}
                disabled={loading}
                className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Iniciando...' : 'Iniciar Sesión'}
              </button>
            </div>
          </div>

          {/* Register Form */}
          <div className="border-t pt-6">
            <h2 className="text-xl font-semibold mb-4">Registrarse</h2>
            <div className="space-y-4">
              <input
                type="email"
                placeholder="Email"
                value={registerForm.email}
                onChange={(e) => setRegisterForm({...registerForm, email: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="text"
                placeholder="Nombre completo"
                value={registerForm.full_name}
                onChange={(e) => setRegisterForm({...registerForm, full_name: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="password"
                placeholder="Contraseña"
                value={registerForm.password}
                onChange={(e) => setRegisterForm({...registerForm, password: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              />
              <select
                value={registerForm.role}
                onChange={(e) => setRegisterForm({...registerForm, role: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="user">Usuario</option>
                <option value="admin">Administrador</option>
              </select>
              <button
                onClick={handleRegister}
                disabled={loading}
                className="w-full bg-green-600 text-white p-3 rounded-lg hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Registrando...' : 'Registrarse'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderDashboard = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Mis Cuentas</h2>
        <button
          onClick={createAccount}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus size={20} />
          Nueva Cuenta
        </button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {accounts.map((account) => (
          <div key={account.id} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <CreditCard className="text-blue-600" size={24} />
              <span className="text-sm text-gray-500">ID: {account.id}</span>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-gray-600">Número de cuenta</p>
              <p className="font-mono text-sm">{account.account_number}</p>
              <p className="text-sm text-gray-600">Saldo</p>
              <p className="text-2xl font-bold text-green-600">${account.balance.toFixed(2)}</p>
            </div>
            <button
              onClick={() => {
                fetchTransactions(account.id);
                setCurrentView('transactions');
              }}
              className="mt-4 w-full bg-gray-100 text-gray-700 py-2 rounded-lg hover:bg-gray-200"
            >
              Ver Historial
            </button>
          </div>
        ))}
      </div>

      {accounts.length === 0 && (
        <div className="text-center py-12">
          <CreditCard size={48} className="mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500">No tienes cuentas bancarias</p>
          <button
            onClick={createAccount}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Crear Primera Cuenta
          </button>
        </div>
      )}
    </div>
  );

  const renderTransactions = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Transacciones</h2>
      
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Transaction Forms */}
        <div className="space-y-6">
          {/* Transfer */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <ArrowUpRight className="text-blue-600" size={20} />
              Transferir
            </h3>
            <div className="space-y-4">
              <select
                value={transactionForm.sender_account_id}
                onChange={(e) => setTransactionForm({...transactionForm, sender_account_id: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg"
                required
              >
                <option value="">Cuenta origen</option>
                {accounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.account_number} - ${account.balance.toFixed(2)}
                  </option>
                ))}
              </select>
              <input
                type="number"
                step="0.01"
                placeholder="ID cuenta destino"
                value={transactionForm.receiver_account_id}
                onChange={(e) => setTransactionForm({...transactionForm, receiver_account_id: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg"
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="Monto"
                value={transactionForm.amount}
                onChange={(e) => setTransactionForm({...transactionForm, amount: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg"
                required
              />
              <button
                onClick={handleTransaction}
                className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700"
              >
                Transferir
              </button>
            </div>
          </div>

          {/* Deposit */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <ArrowDownLeft className="text-green-600" size={20} />
              Depositar
            </h3>
            <div className="space-y-4">
              <select
                value={transactionForm.receiver_account_id}
                onChange={(e) => setTransactionForm({...transactionForm, receiver_account_id: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg"
                required
              >
                <option value="">Seleccionar cuenta</option>
                {accounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.account_number}
                  </option>
                ))}
              </select>
              <input
                type="number"
                step="0.01"
                placeholder="Monto a depositar"
                value={transactionForm.amount}
                onChange={(e) => setTransactionForm({...transactionForm, amount: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg"
                required
              />
              <button
                onClick={handleDeposit}
                className="w-full bg-green-600 text-white p-3 rounded-lg hover:bg-green-700"
              >
                Depositar
              </button>
            </div>
          </div>

          {/* Withdraw */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <ArrowUpRight className="text-red-600" size={20} />
              Retirar
            </h3>
            <div className="space-y-4">
              <select
                value={transactionForm.sender_account_id}
                onChange={(e) => setTransactionForm({...transactionForm, sender_account_id: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg"
                required
              >
                <option value="">Seleccionar cuenta</option>
                {accounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.account_number} - ${account.balance.toFixed(2)}
                  </option>
                ))}
              </select>
              <input
                type="number"
                step="0.01"
                placeholder="Monto a retirar"
                value={transactionForm.amount}
                onChange={(e) => setTransactionForm({...transactionForm, amount: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg"
                required
              />
              <button
                onClick={handleWithdraw}
                className="w-full bg-red-600 text-white p-3 rounded-lg hover:bg-red-700"
              >
                Retirar
              </button>
            </div>
          </div>
        </div>

        {/* Transaction History */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Historial</h3>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {transactions.map((transaction) => (
              <div key={transaction.id} className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium">${transaction.amount.toFixed(2)}</p>
                    <p className="text-sm text-gray-600">
                      {transaction.sender_account_id} → {transaction.receiver_account_id}
                    </p>
                    <p className="text-xs text-gray-500">{transaction.status}</p>
                  </div>
                  <span className="text-xs text-gray-500">
                    {new Date(transaction.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderLogs = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Logs de Acceso</h2>
        <button
          onClick={fetchLogs}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Actualizar
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="space-y-2 p-6 max-h-96 overflow-y-auto">
          {logs.map((log) => (
            <div key={log.id} className="border-l-4 border-green-500 pl-4 py-2">
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-medium">{log.action}</p>
                  <p className="text-sm text-gray-600">IP: {log.ip_address}</p>
                  <p className="text-xs text-gray-500">{log.user_agent}</p>
                </div>
                <span className="text-xs text-gray-500">
                  {new Date(log.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  if (!token) {
    return renderAuthForms();
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold text-gray-900">🏦 UniBank</h1>
              <nav className="flex space-x-4">
                <button
                  onClick={() => setCurrentView('dashboard')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentView === 'dashboard' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <CreditCard size={16} className="inline mr-2" />
                  Cuentas
                </button>
                <button
                  onClick={() => setCurrentView('transactions')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentView === 'transactions' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <ArrowUpRight size={16} className="inline mr-2" />
                  Transacciones
                </button>
                <button
                  onClick={() => setCurrentView('logs')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentView === 'logs' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Activity size={16} className="inline mr-2" />
                  Logs
                </button>
              </nav>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 text-gray-500 hover:text-gray-700"
            >
              <LogOut size={16} />
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Message Display */}
        {message && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg flex items-center gap-2">
            <AlertCircle size={16} className="text-blue-600" />
            <span className="text-blue-800">{message}</span>
            <button
              onClick={() => setMessage('')}
              className="ml-auto text-blue-600 hover:text-blue-800"
            >
              ×
            </button>
          </div>
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="mb-6 text-center">
            <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          </div>
        )}

        {/* Content based on current view */}
        {currentView === 'dashboard' && renderDashboard()}
        {currentView === 'transactions' && renderTransactions()}
        {currentView === 'logs' && renderLogs()}
      </main>
    </div>
  );
};

export default UniBank;