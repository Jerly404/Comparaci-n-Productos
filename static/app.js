// BuscaFono PE - Client Application Logic

const state = {
    stores: [],
    selectedStores: new Set(),
    results: [],
    stats: null,
    storeBreakdown: {},
    loading: false
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

// Initialize application
document.addEventListener("DOMContentLoaded", async () => {
    await fetchStores();
    setupEventListeners();
});

// Fetch supported stores from API
async function fetchStores() {
    try {
        const resp = await fetch("/api/stores");
        if (resp.ok) {
            state.stores = await resp.json();
            // Default select all stores
            state.stores.forEach(s => state.selectedStores.add(s.id));
            renderStoreToggles();
        }
    } catch (e) {
        console.error("Error loading stores:", e);
    }
}

// Render store checkboxes / filter badges
function renderStoreToggles() {
    storeTogglesContainer.innerHTML = "";
    state.stores.forEach(store => {
        const label = document.createElement("label");
        label.className = "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-800 border border-slate-700 hover:border-slate-500 cursor-pointer select-none transition text-slate-300";
        
        const isChecked = state.selectedStores.has(store.id);
        label.innerHTML = `
            <input type="checkbox" value="${store.id}" ${isChecked ? 'checked' : ''} class="w-3.5 h-3.5 rounded text-emerald-500 bg-slate-900 border-slate-700 focus:ring-0">
            <span class="w-2 h-2 rounded-full" style="background-color: ${store.color}"></span>
            <span>${store.name}</span>
        `;

        const checkbox = label.querySelector("input");
        checkbox.addEventListener("change", (e) => {
            if (e.target.checked) {
                state.selectedStores.add(store.id);
            } else {
                state.selectedStores.delete(store.id);
            }
            // If already searched, re-search with updated stores
            if (searchInput.value.trim()) {
                performSearch();
            }
        });

        storeTogglesContainer.appendChild(label);
    });
}

function setupEventListeners() {
    // Search form submit
    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        performSearch();
    });

    // Clear search button
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

    // Quick suggestion chips
    document.querySelectorAll(".quick-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const query = chip.dataset.query;
            searchInput.value = query;
            clearBtn.classList.remove("hidden");
            performSearch();
        });
    });

    // Sorting change
    sortSelect.addEventListener("change", () => {
        if (state.results.length > 0) {
            performSearch();
        }
    });

    // Filters toggles change
    toggleAccessories.addEventListener("change", () => {
        if (searchInput.value.trim()) performSearch();
    });

    toggleRefurbished.addEventListener("change", () => {
        if (searchInput.value.trim()) performSearch();
    });

    // Select all stores button
    selectAllStoresBtn.addEventListener("click", () => {
        state.stores.forEach(s => state.selectedStores.add(s.id));
        renderStoreToggles();
        if (searchInput.value.trim()) performSearch();
    });

    // Export CSV
    exportCsvBtn.addEventListener("click", exportToCsv);
}

// Perform search request to FastAPI backend
async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return;

    state.loading = true;
    updateUIState("loading");

    const storesParam = Array.from(state.selectedStores).join(",");
    const sortParam = sortSelect.value;
    const hideAccessories = toggleAccessories.checked;
    const includeRefurbished = toggleRefurbished.checked;

    const params = new URLSearchParams({
        q: query,
        sort: sortParam,
        hide_accessories: hideAccessories,
        include_refurbished: includeRefurbished
    });
    if (storesParam) {
        params.append("stores", storesParam);
    }

    try {
        const resp = await fetch(`/api/search?${params.toString()}`);
        if (!resp.ok) throw new Error("Search request failed");
        
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

    if (view === "loading") {
        loadingState.classList.remove("hidden");
    } else if (view === "results") {
        resultsWrapper.classList.remove("hidden");
    } else if (view === "empty") {
        emptyState.classList.remove("hidden");
    }
}

// Format currency in Soles S/
function formatPrice(val) {
    if (val == null || isNaN(val)) return "S/ 0.00";
    return `S/ ${Number(val).toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

// Render search results, best deal card and stats
function renderResults() {
    // 1. Stats strip
    statLowest.textContent = formatPrice(state.stats.lowest_price);
    statAverage.textContent = formatPrice(state.stats.average_price);
    statHighest.textContent = formatPrice(state.stats.highest_price);
    statTotal.textContent = `${state.stats.total_results} opciones`;
    resultsCountBadge.textContent = `${state.results.length} teléfonos`;

    // 2. Best Deal Card Highlight (#1 Cheapest Phone)
    const cheapest = state.stats.cheapest_item;
    if (cheapest) {
        const savingsVsAvg = state.stats.average_price > cheapest.price 
            ? Math.round(state.stats.average_price - cheapest.price) 
            : 0;

        bestDealContainer.innerHTML = `
            <div class="best-deal-card rounded-2xl p-5 sm:p-6 relative overflow-hidden flex flex-col sm:flex-row items-center gap-6">
                <!-- Trophy Badge -->
                <div class="absolute -top-1 -right-1 bg-gradient-to-l from-emerald-500 to-teal-500 text-white font-extrabold text-[11px] px-4 py-1 rounded-bl-xl shadow-md uppercase tracking-wider flex items-center gap-1.5">
                    <i class="fa-solid fa-trophy text-amber-300"></i> MEJOR PRECIO ENCONTRADO
                </div>

                <!-- Product Image -->
                <div class="w-36 h-36 flex-shrink-0 bg-slate-900/60 rounded-xl p-2 border border-slate-700/50 flex items-center justify-center">
                    <img 
                        src="${cheapest.image_url || '/static/placeholder.png'}" 
                        alt="${escapeHtml(cheapest.title)}"
                        class="max-w-full max-h-full object-contain hover:scale-105 transition"
                        onerror="this.src='https://placehold.co/200x200/1e293b/94a3b8?text=Celular'"
                    />
                </div>

                <!-- Product Info & Actions -->
                <div class="flex-1 space-y-2 text-center sm:text-left">
                    <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                        <span class="px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wider text-white" style="background-color: ${cheapest.store_color}">
                            ${cheapest.store}
                        </span>
                        <span class="px-2 py-0.5 rounded text-xs font-semibold ${cheapest.condition === 'Nuevo' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'}">
                            ${cheapest.condition}
                        </span>
                        ${cheapest.discount_percent ? `<span class="px-2 py-0.5 rounded text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">-${cheapest.discount_percent}%</span>` : ''}
                    </div>

                    <h2 class="text-lg sm:text-xl font-bold text-white leading-snug">
                        ${escapeHtml(cheapest.title)}
                    </h2>

                    <div class="flex flex-wrap items-baseline justify-center sm:justify-start gap-3 pt-1">
                        <span class="text-3xl font-extrabold text-emerald-400">
                            ${formatPrice(cheapest.price)}
                        </span>
                        ${cheapest.original_price ? `
                            <span class="text-sm text-slate-400 line-through">
                                ${formatPrice(cheapest.original_price)}
                            </span>
                        ` : ''}
                        ${savingsVsAvg > 0 ? `
                            <span class="text-xs text-emerald-300 bg-emerald-950/60 border border-emerald-800/60 px-2 py-0.5 rounded-md font-medium">
                                Ahorras S/ ${savingsVsAvg.toLocaleString()} vs promedio
                            </span>
                        ` : ''}
                    </div>

                    <div class="pt-2">
                        <a 
                            href="${cheapest.url}" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            class="inline-flex items-center gap-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-5 py-2.5 rounded-xl shadow-lg shadow-emerald-500/25 transition text-sm"
                        >
                            <span>Comprar al Menor Precio en ${cheapest.store}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    // 3. Store Breakdown Chips
    storeStatsRow.innerHTML = "";
    Object.keys(state.storeBreakdown).forEach(sId => {
        const info = state.storeBreakdown[sId];
        if (info.count > 0) {
            const badge = document.createElement("div");
            badge.className = "flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800/80 border border-slate-700/80 text-xs";
            badge.innerHTML = `
                <span class="w-2.5 h-2.5 rounded-full" style="background-color: ${info.color}"></span>
                <span class="font-semibold text-slate-200">${info.name}</span>
                <span class="bg-slate-700 text-slate-300 font-bold px-1.5 py-0.2 rounded-full text-[10px]">${info.count}</span>
                <span class="text-emerald-400 font-bold">desde ${formatPrice(info.lowest_price)}</span>
            `;
            storeStatsRow.appendChild(badge);
        }
    });

    // 4. Products Grid (Ordered Lowest to Highest)
    productGrid.innerHTML = "";
    state.results.forEach((prod, index) => {
        const card = document.createElement("div");
        card.className = "product-card bg-darkcard border border-darkborder rounded-2xl p-4 flex flex-col justify-between relative overflow-hidden group";

        const isRank1 = (index === 0 && sortSelect.value === "asc");

        card.innerHTML = `
            <div>
                <!-- Top Rank & Store Badge -->
                <div class="flex items-center justify-between gap-2 mb-3">
                    <span class="px-2.5 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider text-white shadow-sm" style="background-color: ${prod.store_color}">
                        ${prod.store}
                    </span>
                    <div class="flex items-center gap-1.5">
                        ${isRank1 ? `
                            <span class="bg-amber-400 text-slate-950 font-extrabold text-[10px] px-2 py-0.5 rounded-full uppercase flex items-center gap-1">
                                <i class="fa-solid fa-award"></i> #1 Más Barato
                            </span>
                        ` : `
                            <span class="text-slate-500 font-bold text-xs">#${index + 1}</span>
                        `}
                        <span class="px-2 py-0.5 rounded text-[10px] font-medium ${prod.condition === 'Nuevo' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'}">
                            ${prod.condition}
                        </span>
                    </div>
                </div>

                <!-- Product Thumbnail -->
                <div class="w-full h-44 bg-slate-900/40 rounded-xl p-3 mb-3 flex items-center justify-center overflow-hidden border border-slate-800/50">
                    <img 
                        src="${prod.image_url || '/static/placeholder.png'}" 
                        alt="${escapeHtml(prod.title)}"
                        class="max-w-full max-h-full object-contain group-hover:scale-105 transition duration-300"
                        onerror="this.src='https://placehold.co/200x200/1e293b/94a3b8?text=Celular'"
                    />
                </div>

                <!-- Title & Brand -->
                <div class="space-y-1">
                    <span class="text-[11px] text-slate-400 font-medium uppercase tracking-wider block">
                        ${prod.brand || 'Smartphone'}
                    </span>
                    <h3 class="text-sm font-semibold text-slate-100 line-clamp-2 leading-snug group-hover:text-emerald-400 transition" title="${escapeHtml(prod.title)}">
                        ${escapeHtml(prod.title)}
                    </h3>
                </div>
            </div>

            <!-- Price & Buy Button Footer -->
            <div class="pt-4 border-t border-slate-800/80 mt-4 space-y-3">
                <div class="flex items-baseline justify-between">
                    <div>
                        <div class="text-xl font-extrabold ${isRank1 ? 'text-emerald-400' : 'text-slate-100'}">
                            ${formatPrice(prod.price)}
                        </div>
                        ${prod.original_price ? `
                            <div class="text-xs text-slate-500 line-through">
                                ${formatPrice(prod.original_price)}
                            </div>
                        ` : ''}
                    </div>

                    ${prod.discount_percent ? `
                        <span class="text-xs font-bold text-rose-400 bg-rose-500/10 border border-rose-500/30 px-2 py-0.5 rounded">
                            -${prod.discount_percent}%
                        </span>
                    ` : ''}
                </div>

                <a 
                    href="${prod.url}" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="w-full flex items-center justify-center gap-2 bg-slate-800 hover:bg-emerald-600 hover:text-white text-slate-200 text-xs font-semibold py-2.5 rounded-xl border border-slate-700 hover:border-emerald-500 transition duration-200"
                >
                    <span>Ver en ${prod.store}</span>
                    <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                </a>
            </div>
        `;

        productGrid.appendChild(card);
    });
}

// Export to CSV
function exportToCsv() {
    if (!state.results || state.results.length === 0) return;

    const headers = ["Ranking", "Tienda", "Titulo", "Condicion", "Precio_PEN", "Precio_Original", "Descuento", "Enlace"];
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
    link.setAttribute("download", `comparativa_celulares_${searchInput.value.trim().replace(/\s+/g, '_')}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Utility to escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
