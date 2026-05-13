new_css = """    <style>
        :root {
            --f:          'Inter', sans-serif;
            --mono:       'DM Mono', monospace;
            --green:      #166534;
            --green-mid:  #15803d;
            --green-lite: #22c55e;
            --gold:       #ca8a04;
            --gold-lite:  #fbbf24;
            --bg:         #080e0a;
            --bg2:        #0f1912;
            --bg3:        #141f16;
            --border:     rgba(255,255,255,0.07);
            --border2:    rgba(255,255,255,0.12);
            --text:       #f0fdf4;
            --text2:      rgba(240,253,244,0.55);
            --text3:      rgba(240,253,244,0.3);
            --forest:      #166534;
            --forest-dark: #0f4024;
            --forest-mid:  #15803d;
            --forest-lite: #22c55e;
            --white:       #f0fdf4;
            --gray-50:     #0f1912;
            --gray-100:    #141f16;
            --gray-200:    rgba(255,255,255,0.08);
            --gray-300:    rgba(255,255,255,0.12);
            --gray-400:    rgba(240,253,244,0.35);
            --gray-500:    rgba(240,253,244,0.45);
            --gray-600:    rgba(240,253,244,0.55);
            --gray-700:    rgba(240,253,244,0.7);
            --gray-900:    #f0fdf4;
            --green-50:    rgba(21,128,61,0.1);
            --green-100:   rgba(34,197,94,0.15);
            --green-200:   rgba(34,197,94,0.25);
            --green-700:   #22c55e;
            --red-100:     rgba(239,68,68,0.1);
            --red-600:     #ef4444;
            --orange-100:  rgba(249,115,22,0.1);
            --orange-600:  #f97316;
            --blue-50:     rgba(96,165,250,0.08);
            --blue-100:    rgba(96,165,250,0.15);
            --blue-600:    #60a5fa;
            --radius-sm:   6px;
            --radius-md:   10px;
            --radius-lg:   14px;
        }

        * { margin:0; padding:0; box-sizing:border-box; }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
            font-size: 14px;
            line-height: 1.5;
        }

        .page { display: none; animation: fadeUp 0.3s ease; margin-left: 52px; }
        .page.active { display: block; }

        @keyframes fadeUp {
            from { opacity:0; transform:translateY(12px); }
            to   { opacity:1; transform:translateY(0); }
        }
        @keyframes shimmer {
            0%   { background-position: 0% center; }
            100% { background-position: 200% center; }
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* NAVBAR */
        .app-navbar {
            background: var(--bg);
            height: 60px;
            padding: 0 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--border);
        }

        .app-navbar .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text);
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -0.3px;
            text-decoration: none;
        }

        .app-navbar .logo-icon {
            width: 34px; height: 34px;
            background: linear-gradient(135deg, var(--gold), var(--gold-lite));
            border-radius: 9px;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 2px 10px rgba(251,191,36,0.25);
        }

        /* STEPPER BAR */
        .stepper-bar {
            background: var(--bg3);
            border-bottom: 1px solid var(--border);
            padding: 0 20px;
        }

        .stepper {
            display: flex;
            align-items: center;
            height: 52px;
            max-width: 900px;
        }

        .step-item { display: flex; align-items: center; gap: 8px; }

        .step-circle {
            width: 26px; height: 26px;
            border-radius: 50%;
            border: 1.5px solid var(--border2);
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: 600;
            color: var(--text3);
            flex-shrink: 0;
            transition: all 0.3s ease;
        }

        .step-item.active { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.3); border-radius: 20px; padding: 4px 10px 4px 6px; }
        .step-item.active .step-circle { background: var(--gold-lite); border-color: var(--gold-lite); color: #000; font-weight: 700; }
        .step-item.done .step-circle   { background: var(--green-lite); border-color: var(--green-lite); color: #000; font-size: 11px; }

        .step-info { display: flex; flex-direction: column; }

        .step-lbl {
            font-size: 12px; font-weight: 500;
            color: var(--text3);
            transition: color 0.3s;
        }

        .step-item.active .step-lbl { color: var(--gold-lite); }
        .step-item.done .step-lbl   { color: var(--green-lite); }
        .step-sub-lbl { font-size: 10px; color: var(--text3); }

        .step-line {
            flex: 1;
            height: 1px;
            background: var(--border);
            margin: 0 12px;
            min-width: 24px;
            transition: background 0.3s;
        }

        .step-line.done { background: var(--green-lite); }

        /* APP LAYOUT */
        .app-layout {
            display: grid;
            grid-template-columns: 220px 1fr;
            min-height: calc(100vh - 112px);
        }

        /* SIDEBAR (step nav) */
        .sidebar {
            background: var(--bg2);
            border-right: 1px solid var(--border);
            padding: 20px 16px;
        }

        .sidebar-section-title {
            font-size: 10px; font-weight: 600;
            color: var(--text3);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 10px;
            padding-left: 8px;
        }

        .sidebar-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 10px;
            border-radius: var(--radius-md);
            margin-bottom: 3px;
            font-size: 13px;
            color: var(--text2);
            cursor: pointer;
            transition: background 0.15s;
        }

        .sidebar-item:hover { background: rgba(255,255,255,0.04); }
        .sidebar-item.active { background: rgba(251,191,36,0.1); color: var(--gold-lite); font-weight: 600; }

        .sidebar-badge {
            font-size: 10px;
            padding: 2px 7px;
            border-radius: 10px;
            background: rgba(255,255,255,0.06);
            color: var(--text3);
        }

        .sidebar-badge.done   { background: rgba(34,197,94,0.15); color: var(--green-lite); }
        .sidebar-badge.active { background: rgba(251,191,36,0.15); color: var(--gold-lite); }

        .sidebar-divider { height: 1px; background: var(--border); margin: 14px 0; }

        .sidebar-info-title {
            font-size: 10px; font-weight: 600;
            color: var(--text3);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 10px;
            padding-left: 8px;
        }

        .sidebar-info-row {
            padding: 4px 8px;
            font-size: 12px;
            color: var(--text2);
            display: flex;
            justify-content: space-between;
        }

        .sidebar-info-row span { color: var(--green-lite); font-weight: 600; }

        /* MAIN CONTENT */
        .main-content {
            max-width: 760px;
            margin: 0 auto;
            padding: 28px 32px;
            width: 100%;
        }

        .page-title {
            font-size: 22px; font-weight: 700;
            color: var(--text);
            letter-spacing: -0.3px;
            margin-bottom: 4px;
        }

        .page-sub { font-size: 13px; color: var(--text2); margin-bottom: 24px; }

        /* CARDS */
        .card {
            background: var(--bg2);
            border: 1px solid var(--border2);
            border-radius: var(--radius-lg);
            padding: 20px 24px;
            margin-bottom: 16px;
        }

        .card-title {
            font-size: 11px; font-weight: 600;
            color: var(--text3);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 18px;
            display: flex; align-items: center; gap: 8px;
        }

        .card-title::before {
            content: '';
            width: 3px; height: 13px;
            background: var(--green-lite);
            border-radius: 2px;
            flex-shrink: 0;
        }

        /* FORMS */
        .form-group { margin-bottom: 20px; }

        .form-label {
            display: block;
            font-size: 11px; font-weight: 600;
            color: var(--text3);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-hint { font-size: 11px; color: var(--text3); margin-top: 4px; line-height: 1.4; }

        input[type="text"],
        input[type="number"],
        select {
            width: 100%;
            background: rgba(0,0,0,0.3);
            border: 1px solid var(--border2);
            border-radius: var(--radius-md);
            padding: 11px 14px;
            color: var(--text);
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            transition: border-color 0.2s ease;
            appearance: none;
            -webkit-appearance: none;
        }

        input::placeholder { color: var(--text3); }

        input:focus, select:focus {
            outline: none;
            border-color: var(--gold-lite);
            box-shadow: 0 0 0 3px rgba(251,191,36,0.1);
        }

        select {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2394a3b8' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 12px center;
            padding-right: 32px;
        }

        select option { background: #0f1912; color: #f0fdf4; }

        .form-row   { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        .form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }

        /* MAP */
        .search-wrapper { display: flex; gap: 8px; margin-bottom: 12px; }
        .search-wrapper input { flex: 1; }

        .btn-search {
            background: var(--green-mid);
            color: white;
            border: none;
            padding: 9px 18px;
            border-radius: var(--radius-md);
            font-size: 13px; font-weight: 500;
            cursor: pointer;
            white-space: nowrap;
            font-family: 'Inter', sans-serif;
            transition: background 0.2s;
        }

        .btn-search:hover { background: var(--green-lite); color: #000; }

        #carte {
            width: 100%;
            height: 380px;
            border-radius: 14px;
            border: 1px solid var(--border2);
            overflow: hidden;
        }

        .coords-row { display: flex; gap: 10px; margin: 10px 0; }

        .coord-chip {
            background: var(--bg3);
            border: 1px solid var(--border2);
            border-radius: var(--radius-sm);
            padding: 7px 12px;
            font-size: 12px;
            color: var(--text2);
        }

        .coord-chip strong { color: var(--gold-lite); font-weight: 600; }

        .climate-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 10px; margin-top: 14px; }

        .climate-card {
            background: var(--bg3);
            border: 1px solid var(--border2);
            border-radius: var(--radius-md);
            padding: 14px 10px;
            text-align: center;
            transition: border-color 0.2s;
        }

        .climate-card:hover { border-color: var(--green-lite); }
        .climate-icon { font-size: 20px; margin-bottom: 7px; }

        .climate-value {
            font-family: 'DM Mono', monospace;
            font-size: 18px; font-weight: 700;
            color: var(--gold-lite);
            line-height: 1;
        }

        .climate-label { font-size: 10px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

        /* MESSAGES */
        .msg {
            border-radius: var(--radius-md);
            padding: 9px 12px;
            font-size: 12px;
            margin-top: 6px;
            display: flex; align-items: center; gap: 7px;
            line-height: 1.4;
        }

        .msg-success { background: rgba(34,197,94,0.1);  color: #86efac; border: 1px solid rgba(34,197,94,0.25); }
        .msg-warning { background: rgba(249,115,22,0.1); color: #fed7aa; border: 1px solid rgba(249,115,22,0.25); }
        .msg-info    { background: rgba(96,165,250,0.08); color: #bfdbfe; border: 1px solid rgba(96,165,250,0.2); }
        .msg-green   { background: rgba(34,197,94,0.1);  color: #86efac; border: 1px solid rgba(34,197,94,0.25); }

        .hidden { display: none !important; }

        /* MODE SELECTOR */
        .mode-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }

        .mode-card {
            border: 1px solid var(--border2);
            border-radius: var(--radius-lg);
            padding: 18px 20px;
            cursor: pointer;
            transition: all 0.2s ease;
            background: var(--bg2);
            position: relative;
        }

        .mode-card:hover { border-color: var(--green-lite); }
        .mode-card.selected { border-color: var(--gold-lite); background: rgba(202,138,4,0.1); }

        .mode-check {
            position: absolute; top: 14px; right: 14px;
            width: 20px; height: 20px;
            border-radius: 50%;
            border: 1.5px solid var(--border2);
            display: flex; align-items: center; justify-content: center;
            font-size: 10px;
            transition: all 0.2s;
        }

        .mode-card.selected .mode-check { background: var(--gold-lite); border-color: var(--gold-lite); color: #000; }
        .mode-icon { font-size: 24px; margin-bottom: 10px; }
        .mode-title { font-size: 15px; font-weight: 700; color: var(--text); margin-bottom: 5px; }
        .mode-desc { font-size: 12px; color: var(--text2); line-height: 1.5; }

        /* NAV BUTTONS */
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 24px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }

        .btn-back {
            background: transparent;
            border: 1px solid var(--border2);
            color: var(--text2);
            padding: 9px 22px;
            border-radius: 20px;
            font-size: 13px; font-weight: 500;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s;
        }

        .btn-back:hover { border-color: var(--text2); color: var(--text); }

        .btn-next {
            background: var(--gold-lite);
            border: none;
            color: #000;
            padding: 10px 26px;
            border-radius: 20px;
            font-size: 13px; font-weight: 700;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            transition: background 0.2s;
        }

        .btn-next:hover { background: #fcd34d; }

        .btn-calculate {
            background: var(--gold-lite);
            border: none;
            color: #000;
            padding: 11px 32px;
            border-radius: 20px;
            font-size: 14px; font-weight: 700;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            transition: background 0.2s;
        }

        .btn-calculate:hover { background: #fcd34d; }

        /* LOADING */
        .loading-bar {
            display: flex; align-items: center; gap: 12px;
            padding: 14px 18px;
            background: rgba(34,197,94,0.1);
            border: 1px solid rgba(34,197,94,0.25);
            border-radius: var(--radius-md);
            color: #86efac;
            font-size: 13px; font-weight: 500;
        }

        .spinner {
            width: 16px; height: 16px;
            border: 2px solid rgba(34,197,94,0.25);
            border-top-color: #86efac;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            flex-shrink: 0;
        }

        /* RESULTS */
        .results-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }

        .result-card {
            background: var(--bg2);
            border: 1px solid var(--border2);
            border-radius: var(--radius-lg);
            padding: 20px;
        }

        .result-card-title {
            font-size: 11px; font-weight: 600;
            color: var(--text3);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 14px;
            display: flex; align-items: center; gap: 7px;
        }

        .result-card-title::before {
            content: '';
            width: 3px; height: 12px;
            background: var(--green-lite);
            border-radius: 2px;
            flex-shrink: 0;
        }

        .result-row {
            display: flex; justify-content: space-between; align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
        }

        .result-row:last-child { border-bottom: none; }
        .result-label { color: var(--text2); font-size: 12px; }

        .result-value {
            font-weight: 700;
            color: var(--text);
            font-family: 'DM Mono', monospace;
        }

        .result-value.highlight { color: var(--green-lite); font-size: 17px; }
        .result-unit { font-size: 11px; color: var(--text3); margin-left: 3px; font-family: 'Inter', sans-serif; font-weight: 400; }
        .result-card-full { grid-column: 1 / -1; }

        /* POMPES */
        .pompe-card {
            border: 1px solid var(--border2);
            border-radius: var(--radius-md);
            padding: 16px 18px;
            margin-bottom: 10px;
            display: flex; align-items: center; gap: 14px;
            background: var(--bg2);
            transition: border-color 0.2s;
        }

        .pompe-card:hover { border-color: var(--green-lite); }
        .pompe-card.best  { border-color: var(--gold-lite); background: rgba(202,138,4,0.08); }

        .pompe-rank {
            width: 34px; height: 34px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 13px; font-weight: 700;
            flex-shrink: 0;
        }

        .rank-1 { background: var(--gold-lite); color: #000; }
        .rank-2 { background: rgba(34,197,94,0.2); color: var(--green-lite); }
        .rank-3 { background: rgba(255,255,255,0.06); color: var(--text2); }

        .pompe-info { flex: 1; }
        .pompe-name { font-weight: 600; font-size: 13px; color: var(--text); margin-bottom: 4px; }
        .pompe-specs { display: flex; gap: 14px; font-size: 12px; color: var(--text2); flex-wrap: wrap; }
        .pompe-specs strong { color: var(--text); }

        .pompe-carac-box {
            background: rgba(0,0,0,0.3);
            border: 1px solid var(--border2);
            border-radius: var(--radius-md);
            padding: 16px;
            margin-top: 12px;
        }

        .pompe-carac-title {
            font-size: 11px; font-weight: 600;
            color: var(--gold-lite);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 12px;
        }

        .pompe-carac-desc { margin-top: 10px; font-size: 12px; color: var(--text2); font-style: italic; }

        .option-radio {
            display: flex; align-items: center; gap: 10px;
            cursor: pointer;
            padding: 10px 14px;
            border: 1px solid var(--border2);
            border-radius: var(--radius-md);
            font-size: 13px;
            transition: all 0.2s;
            color: var(--text2);
        }

        .option-radio:hover { border-color: var(--green-lite); background: rgba(34,197,94,0.06); }
        .option-radio input[type="radio"] { width: auto; margin: 0; }

        .btn-pdf {
            background: transparent;
            border: 1px solid var(--border2);
            color: var(--text2);
            padding: 9px 22px;
            border-radius: 20px;
            font-size: 13px; font-weight: 600;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s;
            display: flex; align-items: center; gap: 7px;
        }

        .btn-pdf:hover { border-color: var(--gold-lite); color: var(--gold-lite); }

        /* PAGE BG (legacy) */
        .page-bg {
            position: relative;
            min-height: calc(100vh - 60px);
        }

        /* THIN BAR + PROJ SIDEBAR */
        .thin-bar {
            position: fixed;
            left: 0; top: 0; bottom: 0;
            width: 52px;
            background: var(--bg3);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 14px 0;
            z-index: 150;
        }

        .menu-btn {
            width: 34px; height: 34px;
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--border2);
            border-radius: 8px;
            color: var(--text2);
            cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            transition: background 0.2s, color 0.2s;
            flex-shrink: 0;
        }

        .menu-btn:hover { background: rgba(255,255,255,0.1); color: var(--text); }

        .bar-avatar {
            width: 32px; height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--gold), var(--gold-lite));
            display: flex; align-items: center; justify-content: center;
            font-size: 13px; font-weight: 700; color: #000;
            cursor: pointer; border: none;
            box-shadow: 0 2px 8px rgba(251,191,36,0.3);
            transition: transform 0.2s, box-shadow 0.2s;
            flex-shrink: 0;
        }

        .bar-avatar:hover { transform: scale(1.08); box-shadow: 0 4px 14px rgba(251,191,36,0.45); }

        .proj-sidebar {
            position: fixed;
            left: 52px; top: 0; bottom: 0;
            width: 0;
            background: var(--bg2);
            overflow: hidden;
            transition: width 0.25s ease;
            z-index: 99;
            border-right: 1px solid var(--border);
            box-shadow: 4px 0 24px rgba(0,0,0,0.4);
        }

        .proj-sidebar.open { width: 240px; }
        .proj-sidebar-content { min-width: 240px; height: 100%; display: flex; flex-direction: column; }

        .proj-sidebar-header {
            display: flex; align-items: center; justify-content: space-between;
            padding: 18px 18px 14px;
            border-bottom: 1px solid var(--border);
            flex-shrink: 0;
        }

        .proj-sidebar-title {
            font-size: 11px; font-weight: 700;
            color: var(--text3);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-family: 'Inter', sans-serif;
        }

        .proj-close-btn {
            width: 26px; height: 26px;
            background: rgba(255,255,255,0.04);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text3);
            cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            font-size: 13px;
            transition: all 0.2s;
        }

        .proj-close-btn:hover { background: rgba(255,255,255,0.08); color: var(--text2); }

        .proj-list { flex: 1; overflow-y: auto; padding: 8px 0; }
        .proj-list::-webkit-scrollbar { width: 3px; }
        .proj-list::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

        .proj-item {
            padding: 12px 18px;
            border-bottom: 1px solid var(--border);
            transition: background 0.15s;
        }

        .proj-item:hover { background: rgba(255,255,255,0.03); }

        .proj-name {
            font-size: 13px; font-weight: 600;
            color: var(--text);
            margin-bottom: 3px;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            font-family: 'Inter', sans-serif;
        }

        .proj-meta {
            font-size: 11px; color: var(--text3);
            margin-bottom: 8px;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            font-family: 'DM Mono', monospace;
        }

        .proj-resume-btn {
            display: inline-block; font-size: 11px; font-weight: 700;
            color: var(--green-lite); text-decoration: none;
            transition: color 0.2s;
            font-family: 'Inter', sans-serif;
        }

        .proj-resume-btn:hover { color: #86efac; }

        .proj-no-items {
            padding: 20px 18px; font-size: 12px;
            color: var(--text3); line-height: 1.6;
            font-family: 'Inter', sans-serif;
        }

        .proj-sidebar-footer {
            flex-shrink: 0;
            padding: 14px 18px 18px;
            border-top: 1px solid var(--border);
        }

        .proj-user-row { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }

        .proj-user-avatar {
            width: 30px; height: 30px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--gold), var(--gold-lite));
            display: flex; align-items: center; justify-content: center;
            font-size: 13px; font-weight: 700; color: #000;
            flex-shrink: 0;
        }

        .proj-user-nom {
            font-size: 13px; font-weight: 600;
            color: var(--text2);
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            font-family: 'Inter', sans-serif;
        }

        .proj-logout {
            display: flex; align-items: center; gap: 8px;
            font-size: 12px; font-weight: 600;
            color: #ef4444; text-decoration: none;
            padding: 8px 10px; border-radius: 8px;
            background: rgba(239,68,68,0.06);
            border: 1px solid rgba(239,68,68,0.18);
            transition: all 0.2s;
            font-family: 'Inter', sans-serif;
        }

        .proj-logout:hover { background: rgba(239,68,68,0.12); border-color: rgba(239,68,68,0.35); }

        .proj-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 98; }
        .proj-overlay.visible { display: block; }

        /* RESPONSIVE */
        @media (max-width: 1024px) {
            .page { margin-left: 52px; }
            .main-content { max-width: 100%; padding: 20px 20px; }
            .app-layout { grid-template-columns: 180px 1fr; }
        }

        @media (max-width: 768px) {
            .thin-bar { width: 44px; }
            .proj-sidebar { left: 44px; }
            .proj-sidebar.open { width: calc(100vw - 44px); }
            .page { margin-left: 44px; }
            .stepper { overflow-x: auto; padding-bottom: 4px; }
            .stepper::-webkit-scrollbar { height: 3px; }
            .stepper::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }
            .step-lbl, .step-sub-lbl { white-space: nowrap; }
            .main-content { padding: 16px 12px; }
            .app-layout { grid-template-columns: 1fr; }
            .sidebar { display: none; }
            #carte { height: 300px; }
            .climate-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
        }

        @media (max-width: 480px) {
            .thin-bar { width: 44px; }
            .page { margin-left: 44px; }
            .main-content { padding: 12px 8px; }
            #carte { height: 240px; }
            .climate-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
            .nav-buttons { flex-direction: column; gap: 8px; }
            .btn-back, .btn-next { width: 100%; }
        }
    </style>"""

with open('D:/Pompage/templates/dimensionnement.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_font = '    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>'
new_font = '    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=DM+Mono:ital,wght@0,400;0,500&display=swap" rel="stylesheet"/>'
content = content.replace(old_font, new_font)

style_start = content.find('\n    <style>')
style_end = content.find('\n    </style>') + len('\n    </style>')

if style_start == -1 or style_end == -1:
    print("ERROR: Could not find style block boundaries")
    exit(1)

content = content[:style_start] + '\n' + new_css + content[style_end:]

with open('D:/Pompage/templates/dimensionnement.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("Lines:", len(content.split('\n')))
print("Inter font link present:", new_font in content)
print("Old Poppins font still present:", old_font in content)
print("Poppins still in CSS:", "'Poppins'" in content[:content.find('<body')])
