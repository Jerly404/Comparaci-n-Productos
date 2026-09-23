// BuscaFono - Luxury Dark & Champagne Gold / Platinum Edition

const state = {
    stores: [],
    selectedStores: new Set(),
    results: [],
    stats: null,
    storeBreakdown: {},
    loading: false,
    events: [],
    activeView: "comparator"
};

// DOM Elements
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const clearBtn = document.getElementById("clear-btn");
const submitBtn = document.getElementById("submit-btn");
const sortSelect = document.getElementById("sort-select");
const toggleAccessories = document.getElementById("toggle-accessories");
const toggleRefurbished = document.getElementById("toggle-refurbished");
const storeTogglesContainer = document.getElementById("store-toggles");
const selectAllStoresBtn = document.getElementById("select-all-stores");

const tabComparator = document.getElementById("tab-comparator");
const tabEvents = document.getElementById("tab-events");
const linkToEvents = document.getElementById("link-to-events");
const comparatorView = document.getElementById("comparator-view");
const eventsView = document.getElementById("events-view");
const eventsGrid = document.getElementById("events-grid");
const heroCountdownPill = document.getElementById("hero-countdown-pill");

// Black Friday countdown elements
const bfDays = document.getElementById("bf-days");
const bfHours = document.getElementById("bf-hours");
const bfMinutes = document.getElementById("bf-minutes");
const bfSeconds = document.getElementById("bf-seconds");
const blackFridayBadge = document.getElementById("black-friday-badge");

const loadingState = document.getElementById("loading-state");
const resultsWrapper = document.getElementById("results-wrapper");
const emptyState = document.getElementById("empty-state");
const productGrid = document.getElementById("product-grid");
const bestDealContainer = document.getElementById("best-deal-container");
const storeStatsRow = document.getElementById("store-stats-row");
const exportCsvBtn = document.getElementById("export-csv-btn");

const statLowest = document.getElementById("stat-lowest");
const statAverage = document.getElementById("stat-average");
const statHighest = document.getElementById("stat-highest");
const statTotal = document.getElementById("stat-total");
const resultsCountBadge = document.getElementById("results-count-badge");

const DEFAULT_IMAGE_FALLBACK = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='64' height='64' fill='none' stroke='%238c734b' stroke-width='1.5'%3E%3Crect x='5' y='2' width='14' height='20' rx='2'/%3E%3Cline x1='12' y1='18' x2='12' y2='18.01' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E";

document.addEventListener("DOMContentLoaded", async () => {
    await Promise.all([fetchStores(), fetchEvents()]);
    setupEventListeners();
    startCountdownTimers();
});

async function fetchStores() {
    try {
        const resp = await fetch("/api/stores");
        if (resp.ok) {
            state.stores = await resp.json();
            state.stores.forEach(s => state.selectedStores.add(s.id));
            renderStoreToggles();
        }
    } catch (e) {
        console.error("Error loading stores:", e);
    }
}

async function fetchEvents() {
    try {
        const resp = await fetch("/api/events");
        if (resp.ok) {
            state.events = await resp.json();
            renderEventsGrid();
        }
    } catch (e) {
        console.error("Error loading events:", e);
    }
}

function renderStoreToggles() {
    storeTogglesContainer.innerHTML = "";
    state.stores.forEach(store => {
        const label = document.createElement("label");
        const isChecked = state.selectedStores.has(store.id);
        
        label.className = `inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md border cursor-pointer select-none transition text-xs ${
            isChecked 
                ? 'bg-obsidian-850 border-obsidian-700 text-platinum-200 hover:border-gold-400/40' 
                : 'bg-obsidian-950 border-obsidian-700/50 text-platinum-600 opacity-60 hover:opacity-100'
        }`;
        
        label.innerHTML = `
            <input type="checkbox" value="${store.id}" ${isChecked ? 'checked' : ''} class="hidden">
            <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${store.color || '#c5a880'}"></span>
            <span class="font-medium">${store.name}</span>
        `;

        const checkbox = label.querySelector("input");
        checkbox.addEventListener("change", (e) => {
            if (e.target.checked) {
                state.selectedStores.add(store.id);
            } else {
                state.selectedStores.delete(store.id);
            }
            renderStoreToggles();
            if (searchInput.value.trim()) {
                performSearch();
            }
        });

        storeTogglesContainer.appendChild(label);
    });
}

function setupEventListeners() {
    // Tab switching
    tabComparator.addEventListener("click", () => switchView("comparator"));
    tabEvents.addEventListener("click", () => switchView("events"));
    if (linkToEvents) {
        linkToEvents.addEventListener("click", () => switchView("events"));
    }

    // Search form
    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        performSearch();
    });

    searchInput.addEventListener("input", () => {
        if (searchInput.value.trim().length > 0) {
            clearBtn.classList.remove("hidden");
        } else {
            clearBtn.classList.add("hidden");
        }
    });

    clearBtn.addEventListener("click", () => {
        searchInput.value = "";
        clearBtn.classList.add("hidden");
        searchInput.focus();
    });

    document.querySelectorAll(".quick-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            searchInput.value = chip.dataset.query;
            clearBtn.classList.remove("hidden");
            if (state.activeView !== "comparator") {
                switchView("comparator");
            }
            performSearch();
        });
    });

    sortSelect.addEventListener("change", () => {
        if (state.results.length > 0) performSearch();
    });

    toggleAccessories.addEventListener("change", () => {
        if (searchInput.value.trim()) performSearch();
    });

    toggleRefurbished.addEventListener("change", () => {
        if (searchInput.value.trim()) performSearch();
    });

    selectAllStoresBtn.addEventListener("click", () => {
        state.stores.forEach(s => state.selectedStores.add(s.id));
        renderStoreToggles();
        if (searchInput.value.trim()) performSearch();
    });

    exportCsvBtn.addEventListener("click", exportToCsv);
}

function switchView(viewName) {
    state.activeView = viewName;
    const activeTab = "px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-lg transition text-gold-300 bg-obsidian-850 border border-gold-400/30 font-semibold shadow-sm flex items-center gap-1.5 whitespace-nowrap";
    const inactiveTab = "px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-lg transition text-platinum-400 hover:text-gold-200 hover:bg-obsidian-850 flex items-center gap-1.5 whitespace-nowrap";

    if (viewName === "comparator") {
        comparatorView.classList.remove("hidden");
        eventsView.classList.add("hidden");

        tabComparator.className = activeTab;
        tabEvents.className = inactiveTab;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        comparatorView.classList.add("hidden");
        eventsView.classList.remove("hidden");

        tabEvents.className = activeTab;
        tabComparator.className = inactiveTab;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Live Countdown Timers
function startCountdownTimers() {
    updateAllCountdowns();
    setInterval(updateAllCountdowns, 1000);
}

function getTimeRemaining(targetDateStr) {
    const target = new Date(targetDateStr).getTime();
    const now = new Date().getTime();
    const diff = target - now;

    if (diff <= 0) {
        return { isStarted: true, days: 0, hours: 0, minutes: 0, seconds: 0 };
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    return { isStarted: false, days, hours, minutes, seconds };
}

function updateAllCountdowns() {
    // 1. Black Friday 2026 Countdown
    const bfEvent = state.events.find(e => e.id === "black-friday");
    if (bfEvent && bfDays && bfHours && bfMinutes && bfSeconds) {
        const remaining = getTimeRemaining(bfEvent.start_date);
        bfDays.textContent = String(remaining.days).padStart(2, '0');
        bfHours.textContent = String(remaining.hours).padStart(2, '0');
        bfMinutes.textContent = String(remaining.minutes).padStart(2, '0');
        bfSeconds.textContent = String(remaining.seconds).padStart(2, '0');

        if (heroCountdownPill) {
            heroCountdownPill.textContent = `${remaining.days}d ${remaining.hours}h restantes`;
        }
        if (blackFridayBadge) {
            blackFridayBadge.textContent = `${remaining.days}d`;
        }
    }

    // 2. Individual Event Cards Timers
    document.querySelectorAll(".event-countdown-pill").forEach(el => {
        const targetStr = el.dataset.startDate;
        if (targetStr) {
            const rem = getTimeRemaining(targetStr);
            if (rem.isStarted) {
                el.innerHTML = `<span class="text-emerald-400 font-bold">¡En curso hoy!</span>`;
            } else {
                el.innerHTML = `Faltan <span class="font-bold text-gold-300">${rem.days}d ${rem.hours}h ${rem.minutes}m ${rem.seconds}s</span>`;
            }
        }
    });
}

function renderEventsGrid() {
    if (!eventsGrid || !state.events) return;
    eventsGrid.innerHTML = "";

    state.events.forEach(evt => {
        const card = document.createElement("div");
        card.className = "luxury-card rounded-xl p-4 sm:p-5 flex flex-col justify-between space-y-3.5 sm:space-y-4 shadow-lg";

        const storesList = Array.isArray(evt.stores) ? evt.stores : [];
        const isBlackFriday = evt.id === "black-friday";

        card.innerHTML = `
            <div class="space-y-2.5 sm:space-y-3">
                <div class="flex items-center justify-between gap-2">
                    <span class="text-[9px] sm:text-[10px] font-semibold text-gold-300 bg-gold-900/60 border border-gold-400/40 px-2 py-0.5 rounded uppercase tracking-wider">
                        ${evt.badge}
                    </span>
                    <span class="text-[10px] sm:text-[11px] text-platinum-500 font-mono">
                        ${evt.discount_estimate}
                    </span>
                </div>

                <div class="space-y-1">
                    <h3 class="text-base sm:text-lg font-bold text-white tracking-tight">
                        ${evt.name}
                    </h3>
                    <div class="flex items-center gap-1.5 text-xs text-gold-400/90 font-medium">
                        <i class="fa-regular fa-calendar text-[11px]"></i>
                        <span>${evt.display_date}</span>
                    </div>
                </div>

                <!-- Live countdown badge -->
                <div class="bg-obsidian-950 border border-obsidian-700/80 rounded-lg p-2 sm:p-2.5 flex flex-col xs:flex-row xs:items-center justify-between gap-1 text-xs">
                    <span class="text-platinum-500 text-[10px] sm:text-[11px]">Cuenta regresiva:</span>
                    <div class="event-countdown-pill text-xs font-mono text-platinum-300" data-start-date="${evt.start_date}">
                        Cargando...
                    </div>
                </div>

                <p class="text-xs text-platinum-400 leading-relaxed">
                    ${evt.description}
                </p>

                <!-- Participating Stores -->
                <div class="space-y-1.5 pt-1">
                    <span class="text-[10px] uppercase tracking-wider text-platinum-500 block font-semibold">
                        Tiendas participantes:
                    </span>
                    <div class="flex flex-wrap gap-1 text-[11px] text-platinum-400">
                        ${storesList.slice(0, 5).map(s => `
                            <span class="px-2 py-0.5 rounded bg-obsidian-850 border border-obsidian-700 text-platinum-300 text-[10px]">${s}</span>
                        `).join('')}
                        ${storesList.length > 5 ? `<span class="px-1.5 py-0.5 text-[10px] text-platinum-500">+${storesList.length - 5} más</span>` : ''}
                    </div>
                </div>

                <!-- Pro Tip -->
                <div class="bg-obsidian-950/80 border-l-2 border-gold-400/80 p-2.5 rounded-r-lg text-[11px] text-platinum-300 space-y-0.5">
                    <span class="text-gold-300 font-bold uppercase tracking-wider text-[9px] block">Consejo para celulares:</span>
                    <p class="text-platinum-400 text-[11px] leading-snug">${evt.tips}</p>
                </div>
            </div>

            <!-- Action button -->
            <div class="pt-3 border-t border-obsidian-700/60">
                <button type="button" class="btn-platinum-outline w-full py-2 rounded-lg text-xs font-medium flex items-center justify-center gap-1.5 jump-to-compare-btn">
                    <span>Comparar precios actuales</span>
                    <i class="fa-solid fa-arrow-right text-[10px] text-gold-400"></i>
                </button>
            </div>
        `;

        const jumpBtn = card.querySelector(".jump-to-compare-btn");
        jumpBtn.addEventListener("click", () => {
            switchView("comparator");
            searchInput.focus();
        });

        eventsGrid.appendChild(card);
    });

    updateAllCountdowns();
}

async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return;

    state.loading = true;
    updateUIState("loading");

    const storesParam = Array.from(state.selectedStores).join(",");
    const params = new URLSearchParams({
        q: query,
        sort: sortSelect.value,
        hide_accessories: toggleAccessories.checked,
        include_refurbished: toggleRefurbished.checked
    });
    if (storesParam) params.append("stores", storesParam);

    try {
        const resp = await fetch(`/api/search?${params.toString()}`);
        if (!resp.ok) throw new Error("Search failed");
        
        const data = await resp.json();
        state.results = data.results || [];
        state.stats = data.stats || {};
        state.storeBreakdown = data.stores || {};

        if (state.results.length === 0) {
            updateUIState("empty");
        } else {
            updateUIState("results");
            renderResults();
        }
    } catch (err) {
        console.error("Search error:", err);
        updateUIState("empty");
    } finally {
        state.loading = false;
    }
}

function updateUIState(view) {
    loadingState.classList.add("hidden");
    resultsWrapper.classList.add("hidden");
    emptyState.classList.add("hidden");

    if (view === "loading") loadingState.classList.remove("hidden");
    else if (view === "results") resultsWrapper.classList.remove("hidden");
    else if (view === "empty") emptyState.classList.remove("hidden");
}

function formatPrice(val) {
    if (val == null || isNaN(val)) return "S/ 0.00";
    return `S/ ${Number(val).toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function renderResults() {
    // 1. Metric values
    statLowest.textContent = formatPrice(state.stats.lowest_price);
    statAverage.textContent = formatPrice(state.stats.average_price);
    statHighest.textContent = formatPrice(state.stats.highest_price);
    statTotal.textContent = `${state.stats.total_results}`;
    resultsCountBadge.textContent = `${state.results.length} ofertas`;

    // 2. Best Deal Spotlight (Luxury Card)
    const cheapest = state.stats.cheapest_item;
    if (cheapest) {
        const diff = state.stats.average_price > cheapest.price 
            ? Math.round(state.stats.average_price - cheapest.price) 
            : 0;

        bestDealContainer.innerHTML = `
            <div class="best-deal-luxury rounded-xl p-3.5 sm:p-5 flex flex-col sm:flex-row items-center sm:items-stretch gap-4 sm:gap-5 h-full">
                <div class="w-24 h-24 xs:w-28 xs:h-28 sm:w-36 sm:h-36 flex-shrink-0 bg-obsidian-950 rounded-lg p-2.5 border border-obsidian-700/80 flex items-center justify-center">
                    <img 
                        src="${cheapest.image_url || DEFAULT_IMAGE_FALLBACK}" 
                        alt="${escapeHtml(cheapest.title)}"
                        class="max-w-full max-h-full object-contain"
                        onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'"
                    />
                </div>

                <div class="flex-1 space-y-2 text-center sm:text-left flex flex-col justify-between w-full">
                    <div>
                        <div class="flex flex-wrap items-center justify-center sm:justify-start gap-1.5 sm:gap-2">
                            <span class="text-[9px] sm:text-[10px] font-semibold text-gold-300 bg-gold-900/60 border border-gold-400/40 px-2 py-0.5 rounded uppercase tracking-wider">
                                Mejor Precio
                            </span>
                            <span class="text-[10px] sm:text-[11px] font-medium text-platinum-300 bg-obsidian-850 border border-obsidian-700 px-2 py-0.5 rounded flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${cheapest.store_color}"></span>
                                ${cheapest.store}
                            </span>
                            <span class="text-[9px] sm:text-[10px] uppercase tracking-wider text-platinum-400 bg-obsidian-950 border border-obsidian-700 px-2 py-0.5 rounded">
                                ${cheapest.condition}
                            </span>
                        </div>

                        <h2 class="text-sm sm:text-base lg:text-lg font-semibold text-white leading-snug mt-1.5">
                            ${escapeHtml(cheapest.title)}
                        </h2>

                        <div class="flex flex-wrap items-baseline justify-center sm:justify-start gap-2 pt-1">
                            <span class="text-xl sm:text-2xl font-bold text-gold-300">
                                ${formatPrice(cheapest.price)}
                            </span>
                            ${cheapest.original_price ? `
                                <span class="text-xs text-platinum-500 line-through">
                                    ${formatPrice(cheapest.original_price)}
                                </span>
                            ` : ''}
                            ${diff > 0 ? `
                                <span class="text-xs text-gold-400 font-medium">
                                    S/ ${diff.toLocaleString()} por debajo del promedio
                                </span>
                            ` : ''}
                        </div>
                    </div>

                    <div class="pt-2 sm:pt-1.5">
                        <a 
                            href="${cheapest.url}" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            class="btn-gold w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-xs uppercase tracking-wider shadow-md"
                        >
                            <span>Ir a la oferta en ${cheapest.store}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    // 3. Store Breakdown Pills
    storeStatsRow.innerHTML = "";
    Object.keys(state.storeBreakdown).forEach(sId => {
        const info = state.storeBreakdown[sId];
        if (info.count > 0) {
            const pill = document.createElement("div");
            pill.className = "flex items-center gap-1.5 sm:gap-2 px-2 sm:px-2.5 py-1 rounded-md bg-obsidian-900 border border-obsidian-700/70 text-[11px] sm:text-xs text-platinum-400";
            pill.innerHTML = `
                <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${info.color}"></span>
                <span class="font-medium text-platinum-300">${info.name}</span>
                <span class="text-platinum-600">(${info.count})</span>
                <span class="text-gold-300 font-medium">desde ${formatPrice(info.lowest_price)}</span>
            `;
            storeStatsRow.appendChild(pill);
        }
    });

    // 4. Products Grid (Ranked lowest to highest)
    productGrid.innerHTML = "";
    state.results.forEach((prod, index) => {
        const card = document.createElement("div");
        card.className = "luxury-card rounded-xl p-3 sm:p-4 flex flex-col justify-between";

        const isRank1 = (index === 0 && sortSelect.value === "asc");

        card.innerHTML = `
            <div>
                <!-- Top Info -->
                <div class="flex items-center justify-between gap-1.5 mb-2 sm:mb-2.5">
                    <div class="flex items-center gap-1.5 text-[10px] sm:text-[11px] font-medium text-platinum-300 truncate">
                        <span class="w-1.5 h-1.5 rounded-full flex-shrink-0" style="background-color: ${prod.store_color}"></span>
                        <span class="truncate">${prod.store}</span>
                    </div>
                    <div class="flex items-center gap-1 sm:gap-1.5 text-[10px] sm:text-[11px] flex-shrink-0">
                        ${isRank1 ? `
                            <span class="text-gold-300 font-semibold text-[9px] sm:text-[10px] bg-gold-900/60 border border-gold-400/40 px-1.5 py-0.2 rounded uppercase tracking-wider">
                                Más bajo
                            </span>
                        ` : `
                            <span class="text-platinum-600 font-medium text-[10px]">#${index + 1}</span>
                        `}
                        <span class="text-platinum-500 text-[9px] sm:text-[10px] bg-obsidian-950 border border-obsidian-700/60 px-1.5 py-0.2 rounded">
                            ${prod.condition}
                        </span>
                    </div>
                </div>

                <!-- Product Thumbnail -->
                <div class="w-full h-32 xs:h-36 sm:h-40 bg-obsidian-950 rounded-lg p-2 sm:p-2.5 mb-2.5 sm:mb-3 flex items-center justify-center overflow-hidden border border-obsidian-700/50">
                    <img 
                        src="${prod.image_url || DEFAULT_IMAGE_FALLBACK}" 
                        alt="${escapeHtml(prod.title)}"
                        class="max-w-full max-h-full object-contain"
                        onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'"
                    />
                </div>

                <!-- Title -->
                <div class="space-y-1">
                    <span class="text-[9px] sm:text-[10px] text-platinum-500 font-medium uppercase tracking-wider block">
                        ${prod.brand || 'Smartphone'}
                    </span>
                    <h3 class="text-xs font-medium text-platinum-200 line-clamp-2 leading-snug sm:leading-relaxed" title="${escapeHtml(prod.title)}">
                        ${escapeHtml(prod.title)}
                    </h3>
                </div>
            </div>

            <!-- Price & Link Button -->
            <div class="pt-2.5 sm:pt-3 border-t border-obsidian-700/60 mt-2.5 sm:mt-3 space-y-2 sm:space-y-2.5">
                <div class="flex items-baseline justify-between gap-1">
                    <div>
                        <div class="text-base sm:text-lg font-bold ${isRank1 ? 'text-gold-300' : 'text-white'}">
                            ${formatPrice(prod.price)}
                        </div>
                        ${prod.original_price ? `
                            <div class="text-[10px] sm:text-[11px] text-platinum-500 line-through">
                                ${formatPrice(prod.original_price)}
                            </div>
                        ` : ''}
                    </div>

                    ${prod.discount_percent ? `
                        <span class="text-[9px] sm:text-[10px] font-semibold text-gold-300 bg-gold-900/40 border border-gold-400/30 px-1.5 py-0.5 rounded">
                            -${prod.discount_percent}%
                        </span>
                    ` : ''}
                </div>

                <a 
                    href="${prod.url}" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="btn-platinum-outline w-full flex items-center justify-center gap-1.5 text-xs font-medium py-1.5 sm:py-2 rounded-lg"
                >
                    <span>Ver en ${prod.store}</span>
                    <i class="fa-solid fa-arrow-up-right-from-square text-[9px] text-platinum-400"></i>
                </a>
            </div>
        `;

        productGrid.appendChild(card);
    });
}

function exportToCsv() {
    if (!state.results || state.results.length === 0) return;

    const headers = ["Posicion", "Tienda", "Titulo", "Condicion", "Precio_PEN", "Precio_Regular", "Descuento", "URL"];
    const rows = state.results.map((p, idx) => [
        idx + 1,
        `"${p.store}"`,
        `"${(p.title || '').replace(/"/g, '""')}"`,
        `"${p.condition}"`,
        p.price,
        p.original_price || "",
        p.discount_percent ? `${p.discount_percent}%` : "",
        `"${p.url}"`
    ]);

    const csvContent = "data:text/csv;charset=utf-8,\uFEFF" + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `comparativa_${searchInput.value.trim().replace(/\s+/g, '_')}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
