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

        .page { display: none; animation: fadeUp 0.3s ease; }
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

        .accueil-navbar {
            background: var(--bg);
            height: 60px;
            display: flex;
            align-items: center;
            padding: 0 40px;
            position: sticky;
            top: 0;
            z-index: 200;
            border-bottom: 1px solid var(--border);
        }

        .accueil-navbar .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
        }

        .accueil-navbar .logo-icon {
            width: 34px; height: 34px;
            background: linear-gradient(135deg, var(--gold), var(--gold-lite));
            border-radius: 9px;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 2px 12px rgba(251,191,36,0.25);
        }

        .accueil-navbar .logo-text {
            font-size: 18px;
            font-weight: 700;
            color: var(--text);
            letter-spacing: -0.3px;
        }

        .hero {
            position: relative;
            min-height: calc(100vh - 60px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-image: url('/static/images/solar_pump1.jpg');
            background-size: cover;
            background-position: center;
            overflow: hidden;
            padding: 60px 80px;
            width: 100%;
            text-align: center;
        }

        .hero-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(
                160deg,
                rgba(8,14,10,0.92) 0%,
                rgba(8,14,10,0.78) 50%,
                rgba(8,14,10,0.55) 100%
            );
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 700px;
            width: 100%;
        }

        .hero-title {
            font-family: 'Inter', sans-serif;
            font-size: 48px;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -1.5px;
            margin-bottom: 20px;
            color: var(--text);
            text-shadow: 0 2px 20px rgba(0,0,0,0.5);
        }

        .hero-title .shimmer {
            background: linear-gradient(90deg, var(--gold), var(--gold-lite), var(--gold));
            background-size: 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 3s linear infinite;
        }

        .hero-desc {
            font-family: 'Inter', sans-serif;
            font-size: 17px;
            color: var(--text2);
            max-width: 480px;
            margin: 0 auto 40px;
            line-height: 1.8;
        }

        .auth-cards {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
            max-width: 580px;
            margin: 0 auto;
        }

        .auth-card {
            border-radius: 16px;
            padding: 24px 22px;
            cursor: pointer;
            transition: all 0.25s ease;
            text-decoration: none;
            display: block;
            text-align: left;
        }

        .auth-card-green {
            background: rgba(15,25,18,0.7);
            border: 1px solid var(--border2);
            backdrop-filter: blur(8px);
        }

        .auth-card-green:hover {
            background: rgba(21,128,61,0.15);
            border-color: rgba(34,197,94,0.4);
            transform: translateY(-4px);
            box-shadow: 0 16px 40px rgba(0,0,0,0.4);
        }

        .auth-card-gold {
            background: rgba(15,25,18,0.7);
            border: 1px solid rgba(251,191,36,0.25);
            backdrop-filter: blur(8px);
        }

        .auth-card-gold:hover {
            background: rgba(202,138,4,0.15);
            border-color: rgba(251,191,36,0.5);
            transform: translateY(-4px);
            box-shadow: 0 16px 40px rgba(251,191,36,0.15);
        }

        .auth-card-icon { margin-bottom: 12px; }

        .auth-card-title {
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 7px;
        }

        .auth-card-desc {
            font-size: 12px;
            color: var(--text2);
            line-height: 1.6;
            margin-bottom: 16px;
        }

        .auth-btn-green {
            display: block;
            width: 100%;
            background: var(--green-mid);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 9px;
            font-size: 13px;
            font-weight: 700;
            text-align: center;
            font-family: 'Inter', sans-serif;
            transition: background 0.2s;
            text-decoration: none;
        }

        .auth-btn-green:hover { background: var(--green-lite); color: #000; }

        .auth-btn-gold {
            display: block;
            width: 100%;
            background: var(--gold-lite);
            color: #000;
            border: none;
            padding: 10px 16px;
            border-radius: 9px;
            font-size: 13px;
            font-weight: 700;
            text-align: center;
            font-family: 'Inter', sans-serif;
            transition: background 0.2s;
            text-decoration: none;
        }

        .auth-btn-gold:hover { background: #fcd34d; }

        .hero-note {
            position: relative;
            z-index: 2;
            margin-top: 22px;
            font-size: 11px;
            color: var(--text3);
        }

        .app-navbar {
            background: var(--bg2);
            height: 56px;
            padding: 0 32px;
            display: flex;
            align-items: center;
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
            font-size: 16px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }

        .app-navbar .logo-icon {
            width: 30px; height: 30px;
            background: linear-gradient(135deg, var(--gold), var(--gold-lite));
            border-radius: var(--radius-sm);
            display: flex; align-items: center; justify-content: center;
            font-size: 14px;
        }

        .stepper-bar {
            background: var(--bg3);
            border-bottom: 1px solid var(--border);
            padding: 0 32px;
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

        .step-item.active .step-circle { background: var(--gold-lite); border-color: var(--gold-lite); color: #000; }
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

        .app-layout {
            display: flex;
            justify-content: center;
            min-height: calc(100vh - 108px);
        }

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
        .sidebar-item.active { background: rgba(34,197,94,0.08); color: var(--green-lite); font-weight: 500; }

        .sidebar-badge {
            font-size: 10px;
            padding: 2px 7px;
            border-radius: 10px;
            background: rgba(255,255,255,0.06);
            color: var(--text3);
        }

        .sidebar-badge.done   { background: rgba(34,197,94,0.15); color: var(--green-lite); }
        .sidebar-badge.active { background: rgba(34,197,94,0.15); color: var(--green-lite); }

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

        .sidebar-info-row span { color: var(--green-lite); font-weight: 500; }

        .main-content { padding: 28px 32px; max-width: 760px; width: 100%; margin: 0 auto; }

        .page-title {
            font-size: 22px; font-weight: 700;
            color: var(--text);
            letter-spacing: -0.3px;
            margin-bottom: 4px;
        }

        .page-sub { font-size: 13px; color: var(--text2); margin-bottom: 24px; }

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

        .form-group { margin-bottom: 16px; }

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
            background: rgba(0,0,0,0.25);
            border: 1px solid var(--border2);
            border-radius: var(--radius-md);
            padding: 9px 12px;
            color: var(--text);
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            transition: border-color 0.2s ease;
            appearance: none;
            -webkit-appearance: none;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--gold-lite);
            box-shadow: 0 0 0 3px rgba(251,191,36,0.1);
        }

        input::placeholder { color: var(--text3); }

        select {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2394a3b8' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 12px center;
            padding-right: 32px;
        }

        select option { background: #0f1912; color: #f0fdf4; }

        .form-row   { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        .form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }

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
            border-radius: var(--radius-lg);
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

        .coord-chip strong { color: var(--green-lite); font-weight: 600; }

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
            color: var(--green-lite);
            line-height: 1;
        }

        .climate-label { font-size: 10px; color: var(--text3); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

        .msg {
            border-radius: var(--radius-md);
            padding: 9px 12px;
            font-size: 12px;
            margin-top: 6px;
            display: flex; align-items: center; gap: 7px;
            line-height: 1.4;
        }

        .msg-success { background: rgba(34,197,94,0.1);  color: #22c55e; border: 1px solid rgba(34,197,94,0.2); }
        .msg-warning { background: rgba(249,115,22,0.1); color: #f97316; border: 1px solid rgba(249,115,22,0.2); }
        .msg-info    { background: rgba(96,165,250,0.08); color: #60a5fa; border: 1px solid rgba(96,165,250,0.15); }
        .msg-green   { background: rgba(34,197,94,0.1);  color: #22c55e; border: 1px solid rgba(34,197,94,0.2); }

        .hidden { display: none !important; }

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
        .mode-card.selected { border-color: var(--gold-lite); background: rgba(202,138,4,0.08); }

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

        .loading-bar {
            display: flex; align-items: center; gap: 12px;
            padding: 14px 18px;
            background: rgba(34,197,94,0.08);
            border: 1px solid rgba(34,197,94,0.2);
            border-radius: var(--radius-md);
            color: #22c55e;
            font-size: 13px; font-weight: 500;
        }

        .spinner {
            width: 16px; height: 16px;
            border: 2px solid rgba(34,197,94,0.2);
            border-top-color: #22c55e;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            flex-shrink: 0;
        }

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
            background: #22c55e;
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

        .result-value.highlight { color: #22c55e; font-size: 17px; }
        .result-unit { font-size: 11px; color: var(--text3); margin-left: 3px; font-family: 'Inter', sans-serif; font-weight: 400; }
        .result-card-full { grid-column: 1 / -1; }

        .pompe-card {
            border: 1px solid var(--border2);
            border-radius: var(--radius-md);
            padding: 16px 18px;
            margin-bottom: 10px;
            display: flex; align-items: center; gap: 14px;
            background: var(--bg2);
            transition: border-color 0.2s;
        }

        .pompe-card:hover { border-color: #22c55e; }
        .pompe-card.best  { border-color: #22c55e; background: rgba(34,197,94,0.06); }

        .pompe-rank {
            width: 34px; height: 34px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 13px; font-weight: 700;
            flex-shrink: 0;
        }

        .rank-1 { background: var(--gold-lite); color: #000; }
        .rank-2 { background: rgba(34,197,94,0.2); color: #22c55e; }
        .rank-3 { background: rgba(255,255,255,0.06); color: var(--text2); }

        .pompe-info { flex: 1; }
        .pompe-name { font-weight: 600; font-size: 13px; color: var(--text); margin-bottom: 4px; }
        .pompe-specs { display: flex; gap: 14px; font-size: 12px; color: var(--text2); flex-wrap: wrap; }
        .pompe-specs strong { color: var(--text); }

        .pompe-carac-box {
            background: rgba(34,197,94,0.06);
            border: 1px solid rgba(34,197,94,0.2);
            border-radius: var(--radius-md);
            padding: 16px;
            margin-top: 12px;
        }

        .pompe-carac-title {
            font-size: 11px; font-weight: 600;
            color: #22c55e;
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

        .option-radio:hover { border-color: #22c55e; background: rgba(34,197,94,0.06); }
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

        .btn-pdf:hover { border-color: #22c55e; color: #22c55e; }

        @media (max-width: 1024px) {
            .hero { padding: 50px 40px !important; }
            .hero-title { font-size: 36px !important; letter-spacing: -0.5px; }
        }

        @media (max-width: 768px) {
            .accueil-navbar { padding: 0 20px; height: 52px; }
            .accueil-navbar .logo-text { font-size: 16px; }
            .hero { padding: 40px 20px !important; min-height: calc(100vh - 52px); }
            .hero-title { font-size: 36px !important; }
            .hero-desc { font-size: 15px; }
            .auth-cards { grid-template-columns: 1fr !important; max-width: 400px; gap: 14px; }
            .auth-btn-green, .auth-btn-gold { padding: 12px 16px; font-size: 14px; }
        }

        @media (max-width: 480px) {
            .accueil-navbar { padding: 0 16px; }
            .hero { padding: 32px 16px !important; }
            .hero-title { font-size: 28px !important; letter-spacing: -0.3px; margin-bottom: 14px; }
            .hero-desc { font-size: 14px; margin-bottom: 28px; }
            .auth-cards { max-width: 100%; }
            .auth-card { padding: 20px 18px; }
            .auth-btn-green, .auth-btn-gold { width: 100%; display: block; text-align: center; padding: 13px 16px; }
        }
    </style>"""

with open('D:/Pompage/templates/index.html', 'r', encoding='utf-8') as f:
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

with open('D:/Pompage/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("Lines:", len(content.split('\n')))
print("Inter font link present:", new_font in content)
print("Old Poppins font still present:", old_font in content)
