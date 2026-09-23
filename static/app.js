// BuscaFono - Luxury Dark & Champagne Gold / Platinum Edition

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

const DEFAULT_IMAGE_FALLBACK = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='64' height='64' fill='none' stroke='%238c734b' stroke-width='1.5'%3E%3Crect x='5' y='2' width='14' height='20' rx='2'/%3E%3Cline x1='12' y1='18' x2='12' y2='18.01' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E";

document.addEventListener("DOMContentLoaded", async () => {
    await fetchStores();
    setupEventListeners();
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
            <div class="best-deal-luxury rounded-xl p-5 flex flex-col sm:flex-row items-center gap-5">
                <div class="w-32 h-32 flex-shrink-0 bg-obsidian-950 rounded-lg p-2.5 border border-obsidian-700/80 flex items-center justify-center">
                    <img 
                        src="${cheapest.image_url || DEFAULT_IMAGE_FALLBACK}" 
                        alt="${escapeHtml(cheapest.title)}"
                        class="max-w-full max-h-full object-contain"
                        onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'"
                    />
                </div>

                <div class="flex-1 space-y-2 text-center sm:text-left">
                    <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                        <span class="text-[10px] font-semibold text-gold-300 bg-gold-900/60 border border-gold-400/40 px-2 py-0.5 rounded uppercase tracking-wider">
                            Mejor Precio
                        </span>
                        <span class="text-[11px] font-medium text-platinum-300 bg-obsidian-850 border border-obsidian-700 px-2 py-0.5 rounded flex items-center gap-1.5">
                            <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${cheapest.store_color}"></span>
                            ${cheapest.store}
                        </span>
                        <span class="text-[10px] uppercase tracking-wider text-platinum-400 bg-obsidian-950 border border-obsidian-700 px-2 py-0.5 rounded">
                            ${cheapest.condition}
                        </span>
                    </div>

                    <h2 class="text-base sm:text-lg font-semibold text-white leading-snug">
                        ${escapeHtml(cheapest.title)}
                    </h2>

                    <div class="flex flex-wrap items-baseline justify-center sm:justify-start gap-2.5 pt-0.5">
                        <span class="text-2xl font-bold text-gold-300">
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

                    <div class="pt-1.5">
                        <a 
                            href="${cheapest.url}" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            class="btn-gold inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xs uppercase tracking-wider shadow-md"
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
            pill.className = "flex items-center gap-2 px-2.5 py-1 rounded-md bg-obsidian-900 border border-obsidian-700/70 text-xs text-platinum-400";
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
        card.className = "luxury-card rounded-xl p-4 flex flex-col justify-between";

        const isRank1 = (index === 0 && sortSelect.value === "asc");

        card.innerHTML = `
            <div>
                <!-- Top Info -->
                <div class="flex items-center justify-between gap-2 mb-2.5">
                    <div class="flex items-center gap-1.5 text-[11px] font-medium text-platinum-300">
                        <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${prod.store_color}"></span>
                        <span>${prod.store}</span>
                    </div>
                    <div class="flex items-center gap-1.5 text-[11px]">
                        ${isRank1 ? `
                            <span class="text-gold-300 font-semibold text-[10px] bg-gold-900/60 border border-gold-400/40 px-1.5 py-0.2 rounded uppercase tracking-wider">
                                Más bajo
                            </span>
                        ` : `
                            <span class="text-platinum-600 font-medium">#${index + 1}</span>
                        `}
                        <span class="text-platinum-500 text-[10px] bg-obsidian-950 border border-obsidian-700/60 px-1.5 py-0.2 rounded">
                            ${prod.condition}
                        </span>
                    </div>
                </div>

                <!-- Product Thumbnail -->
                <div class="w-full h-40 bg-obsidian-950 rounded-lg p-2.5 mb-3 flex items-center justify-center overflow-hidden border border-obsidian-700/50">
                    <img 
                        src="${prod.image_url || DEFAULT_IMAGE_FALLBACK}" 
                        alt="${escapeHtml(prod.title)}"
                        class="max-w-full max-h-full object-contain"
                        onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'"
                    />
                </div>

                <!-- Title -->
                <div class="space-y-1">
                    <span class="text-[10px] text-platinum-500 font-medium uppercase tracking-wider block">
                        ${prod.brand || 'Smartphone'}
                    </span>
                    <h3 class="text-xs font-medium text-platinum-200 line-clamp-2 leading-relaxed" title="${escapeHtml(prod.title)}">
                        ${escapeHtml(prod.title)}
                    </h3>
                </div>
            </div>

            <!-- Price & Link Button -->
            <div class="pt-3 border-t border-obsidian-700/60 mt-3 space-y-2.5">
                <div class="flex items-baseline justify-between">
                    <div>
                        <div class="text-lg font-bold ${isRank1 ? 'text-gold-300' : 'text-white'}">
                            ${formatPrice(prod.price)}
                        </div>
                        ${prod.original_price ? `
                            <div class="text-[11px] text-platinum-500 line-through">
                                ${formatPrice(prod.original_price)}
                            </div>
                        ` : ''}
                    </div>

                    ${prod.discount_percent ? `
                        <span class="text-[10px] font-semibold text-gold-300 bg-gold-900/40 border border-gold-400/30 px-1.5 py-0.5 rounded">
                            -${prod.discount_percent}%
                        </span>
                    ` : ''}
                </div>

                <a 
                    href="${prod.url}" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="btn-platinum-outline w-full flex items-center justify-center gap-1.5 text-xs font-medium py-2 rounded-lg"
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
