from __future__ import annotations

TASK_TITLES = {
    "1": "Задача №1. Проектирование Call-центра.",
    "2": "Задача №2. Проектирование производственного участка.",
}

TASK_INTROS = {
    "1": "Известно, что среднее время между звонками клиентов составляет Tc секунд, а среднее время обслуживания Ts секунд. Все потоки случайных событий считать пуассоновскими.",
    "2": "Имеется участок с N станками. Среднее время между наладками составляет Tc минут, среднее время наладки — Ts минут. Все потоки случайных событий считать пуассоновскими.",
}

SECTION_SPECS = [
    {
        "section_id": "1.1",
        "title": "Система без очереди",
        "task_file": "task_1_1.json",
        "scheme_id": "task1_1__scheme",
        "figure_ids": [
            "task1_1__busy_operators_vs_operators",
            "task1_1__refusal_and_utilization_vs_operators",
        ],
        "statement": "Рассмотреть систему без очереди. Построить графики от числа операторов: вероятности отказа вплоть до обеспечения отказов менее 1%; математического ожидания числа занятых операторов; коэффициента загрузки операторов.",
        "state_formulas": [
            r"a = \lambda / \mu",
            r"p_0 = \left(\sum_{k=0}^{n}\frac{a^k}{k!}\right)^{-1}",
            r"p_k = \frac{a^k}{k!}p_0,\quad k=0,\ldots,n",
        ],
        "metric_formulas": [
            r"P_{\mathrm{отк}} = p_n",
            r"M_{\mathrm{зан}} = \sum_{k=0}^{n}k\,p_k",
            r"K_{\mathrm{загр}} = M_{\mathrm{зан}}/n",
        ],
    },
    {
        "section_id": "1.2",
        "title": "Система с ограниченной очередью",
        "task_file": "task_1_2.json",
        "scheme_id": "task1_2__scheme",
        "figure_ids": [
            "task1_2__refusal_vs_queue__family_by_operators",
            "task1_2__busy_operators_vs_queue__family_by_operators",
            "task1_2__operators_utilization_vs_queue__family_by_operators",
            "task1_2__queue_exists_vs_queue__family_by_operators",
            "task1_2__queue_length_vs_queue__family_by_operators",
            "task1_2__queue_occupancy_vs_queue__family_by_operators",
            "task1_2__refusal_vs_operators__family_by_queue",
            "task1_2__busy_operators_vs_operators__family_by_queue",
            "task1_2__operators_utilization_vs_operators__family_by_queue",
            "task1_2__queue_exists_vs_operators__family_by_queue",
            "task1_2__queue_length_vs_operators__family_by_queue",
            "task1_2__queue_occupancy_vs_operators__family_by_queue",
        ],
        "statement": "Рассмотреть систему с ограниченной очередью. Варьируя число операторов вплоть до 15, построить семейства графиков от числа мест в очереди: вероятности отказа; математического ожидания числа занятых операторов; коэффициента загрузки операторов; вероятности существования очереди; математического ожидания длины очереди; коэффициента занятости мест в очереди. Варьируя число мест в очереди вплоть до 15, построить семейства графиков от числа операторов для тех же метрик.",
        "state_formulas": [
            r"a = \lambda / \mu,\quad \rho_n = \lambda /(n\mu)",
            r"p_0 = \left(\sum_{k=0}^{n}\frac{a^k}{k!} + \frac{a^n}{n!}\sum_{r=1}^{m}\rho_n^{\,r}\right)^{-1}",
            r"p_k = \frac{a^k}{k!}p_0,\quad k=0,\ldots,n",
            r"p_{n+r} = \frac{a^n}{n!}\rho_n^{\,r}p_0,\quad r=1,\ldots,m",
        ],
        "metric_formulas": [
            r"P_{\mathrm{отк}} = p_{n+m}",
            r"M_{\mathrm{зан}} = \sum_{k=0}^{n+m}\min(k,n)\,p_k",
            r"P_{\mathrm{оч}} = \sum_{k=n+1}^{n+m}p_k",
            r"L_{\mathrm{оч}} = \sum_{k=n+1}^{n+m}(k-n)\,p_k,\quad K_{\mathrm{мест}} = L_{\mathrm{оч}}/m",
        ],
    },
    {
        "section_id": "1.3",
        "title": "Система с неограниченной очередью",
        "task_file": "task_1_3.json",
        "scheme_id": "task1_3__scheme",
        "figure_ids": [
            "task1_3__busy_operators_vs_operators",
            "task1_3__operators_utilization_vs_operators",
            "task1_3__queue_exists_vs_operators",
            "task1_3__queue_length_vs_operators",
        ],
        "statement": "Рассмотреть систему без ограничений на длину очереди. Построить графики от числа операторов вплоть до 15: математического ожидания числа занятых операторов; коэффициента загрузки операторов; вероятности существования очереди; математического ожидания длины очереди.",
        "state_formulas": [
            r"a = \lambda / \mu,\quad \rho_n = \lambda /(n\mu)",
            r"p_0 = \left(\sum_{k=0}^{n-1}\frac{a^k}{k!} + \frac{a^n}{n!(1-\rho_n)}\right)^{-1},\quad \rho_n < 1",
            r"P_{\mathrm{wait}} = \frac{a^n}{n!(1-\rho_n)}p_0",
        ],
        "metric_formulas": [
            r"M_{\mathrm{зан}} = a,\quad K_{\mathrm{загр}} = a/n",
            r"P_{\mathrm{оч}} = P_{\mathrm{wait}}\rho_n",
            r"L_{\mathrm{оч}} = \frac{P_{\mathrm{wait}}\rho_n}{1-\rho_n}",
        ],
    },
    {
        "section_id": "1.4",
        "title": "Система с неограниченной очередью и уходом клиентов",
        "task_file": "task_1_4.json",
        "scheme_id": "task1_4__scheme",
        "figure_ids": [
            "task1_4__busy_operators_vs_operators",
            "task1_4__operators_utilization_vs_operators",
            "task1_4__queue_exists_vs_operators",
            "task1_4__queue_length_vs_operators",
        ],
        "statement": "Рассмотреть систему без ограничений на длину очереди, учитывающую фактор ухода клиентов из очереди при среднем приемлемом времени ожидания Tw. Построить графики от числа операторов вплоть до 15: математического ожидания числа занятых операторов; коэффициента загрузки операторов; вероятности существования очереди; математического ожидания длины очереди.",
        "state_formulas": [
            r"\nu = 1/T_w,\quad \beta_k = \lambda",
            r"\delta_k = \min(k,n)\mu + \max(k-n,0)\nu",
            r"p_k = p_{k-1}\beta_k/\delta_k,\quad k \ge 1",
            r"p_0 = \left(1 + \sum_{k=1}^{\infty}\prod_{i=1}^{k}\beta_i/\delta_i\right)^{-1}",
        ],
        "metric_formulas": [
            r"M_{\mathrm{зан}} = \sum_{k=0}^{\infty}\min(k,n)\,p_k,\quad K_{\mathrm{загр}} = M_{\mathrm{зан}}/n",
            r"P_{\mathrm{оч}} = \sum_{k=n+1}^{\infty}p_k",
            r"L_{\mathrm{оч}} = \sum_{k=n+1}^{\infty}(k-n)\,p_k",
        ],
    },
    {
        "section_id": "2.1",
        "title": "Метрики производственного участка по числу наладчиков",
        "task_file": "task_2_1.json",
        "scheme_id": "task2_1__scheme",
        "figure_ids": [
            "task2_1__idle_machines_vs_repairers",
            "task2_1__waiting_machines_vs_repairers",
            "task2_1__waiting_probability_vs_repairers",
            "task2_1__busy_repairers_vs_repairers",
            "task2_1__repairers_utilization_vs_repairers",
        ],
        "statement": "Построить графики от числа наладчиков: математического ожидания числа простаивающих станков; математического ожидания числа станков, ожидающих обслуживания; вероятности ожидания обслуживания; математического ожидания числа занятых наладчиков; коэффициента занятости наладчиков.",
        "state_formulas": [
            r"\lambda_i = (N-i)\lambda,\quad \mu_i = \min(i,r)\mu",
            r"p_i = p_{i-1}\lambda_{i-1}/\mu_i,\quad i=1,\ldots,N",
            r"p_0 = \left(1 + \sum_{i=1}^{N}\prod_{j=1}^{i}\lambda_{j-1}/\mu_j\right)^{-1}",
        ],
        "metric_formulas": [
            r"M_{\mathrm{пр}} = \sum_{i=0}^{N}i\,p_i,\quad M_{\mathrm{ож}} = \sum_{i=0}^{N}\max(i-r,0)\,p_i",
            r"M_{\mathrm{зан}} = \sum_{i=0}^{N}\min(i,r)\,p_i,\quad K_{\mathrm{загр}} = M_{\mathrm{зан}}/r",
            r"P_{\mathrm{ож}} = \frac{\sum_{i=r}^{N-1}(N-i)p_i}{\sum_{i=0}^{N-1}(N-i)p_i}",
        ],
    },
]
