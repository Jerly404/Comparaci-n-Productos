// BUSCAPRODUCTOS PERÚ - Luxury Dark & Champagne Gold / Platinum Edition

function loadFavoritesFromStorage() {
    try {
        const stored = localStorage.getItem("buscaproductos_favorites");
        return stored ? JSON.parse(stored) : [];
    } catch (e) {
        return [];
    }
}

function saveFavoritesToStorage() {
    try {
        localStorage.setItem("buscaproductos_favorites", JSON.stringify(state.favorites));
    } catch (e) {
        console.error("Error saving favorites:", e);
    }
}

const state = {
    stores: [],
    selectedStores: new Set(),
    results: [],
    stats: null,
    storeBreakdown: {},
    loading: false,
    events: [],
    activeView: "comparator", // 'comparator', 'groceries', 'food', 'events'
    paymentFilter: "all", // 'all', 'any_card', 'store_cards'
    verdictFilter: "all", // 'all', 'minimo', 'buen_precio'
    pickupCajamarcaOnly: false,
    productLocation: "cajamarca",
    productOnlyDiscounts: false,
    compareItems: [], // array of up to 2 items for side-by-side
    favorites: loadFavoritesFromStorage(),
    groceries: [],
    groceriesStats: null,
    groceriesCategory: "todas",
    groceriesQuery: "",
    foodCategory: "todas",
    foodPlatform: "todas",
    foodLocation: "todas",
    foodOnlyDiscounts: false,
    foodQuery: "",
    foodSort: "asc",
    foodDeals: [],
    foodStats: null,
    foodCategories: {}
};

// DOM Elements - Phones & Stores
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const clearBtn = document.getElementById("clear-btn");
const submitBtn = document.getElementById("submit-btn");
const sortSelect = document.getElementById("sort-select");
const productLocationSelect = document.getElementById("product-location-select");
const toggleProductOnlyDiscounts = document.getElementById("toggle-product-only-discounts");
const toggleAccessories = document.getElementById("toggle-accessories");
const toggleRefurbished = document.getElementById("toggle-refurbished");
const toggleCajamarcaPickup = document.getElementById("toggle-cajamarca-pickup");
const productPickupLabelText = document.getElementById("product-pickup-label-text");
const productPickupSubtext = document.getElementById("product-pickup-subtext");
const storeTogglesContainer = document.getElementById("store-toggles");
const selectAllStoresBtn = document.getElementById("select-all-stores");

// Top Nav & Views
const tabComparator = document.getElementById("tab-comparator");
const tabGroceries = document.getElementById("tab-groceries");
const tabFood = document.getElementById("tab-food");
const tabEvents = document.getElementById("tab-events");
const linkToEvents = document.getElementById("link-to-events");

const comparatorView = document.getElementById("comparator-view");
const groceriesView = document.getElementById("groceries-view");
const foodView = document.getElementById("food-view");
const eventsView = document.getElementById("events-view");
const eventsGrid = document.getElementById("events-grid");
const heroCountdownPill = document.getElementById("hero-countdown-pill");

// Favorites & Badges
const openFavoritesBtn = document.getElementById("open-favorites-btn");
const favCountBadge = document.getElementById("fav-count-badge");
const favoritesModal = document.getElementById("favorites-modal");
const closeFavoritesModal = document.getElementById("close-favorites-modal");
const closeFavoritesBtnFooter = document.getElementById("close-favorites-btn-footer");
const favoritesList = document.getElementById("favorites-list");
const clearAllFavoritesBtn = document.getElementById("clear-all-favorites");
const favModalCounter = document.getElementById("fav-modal-counter");

// Side-by-Side Comparator
const compareTray = document.getElementById("compare-tray");
const compareTrayPreviews = document.getElementById("compare-tray-previews");
const compareTrayText = document.getElementById("compare-tray-text");
const compareTrayBtn = document.getElementById("compare-tray-btn");
const compareTrayClear = document.getElementById("compare-tray-clear");
const compareModal = document.getElementById("compare-modal");
const closeCompareModal = document.getElementById("close-compare-modal");
const compareModalContent = document.getElementById("compare-modal-content");

// Groceries & Supermarkets
const groceriesSearchInput = document.getElementById("groceries-search-input");
const groceriesClearBtn = document.getElementById("groceries-clear-btn");
const groceriesGrid = document.getElementById("groceries-grid");
const groceriesCountBadge = document.getElementById("groceries-count-badge");
const basketTotalMetro = document.getElementById("basket-total-metro");
const basketTotalTottus = document.getElementById("basket-total-tottus");
const basketTotalPlazavea = document.getElementById("basket-total-plazavea");
const basketMaxSaving = document.getElementById("basket-max-saving");

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

// DOM Elements - Food Deals, Rappi & Yape Promos
const foodSearchInput = document.getElementById("food-search-input");
const foodClearBtn = document.getElementById("food-clear-btn");
const foodSortSelect = document.getElementById("food-sort-select");
const foodLocationSelect = document.getElementById("food-location-select");
const toggleFoodOnlyDiscounts = document.getElementById("toggle-food-only-discounts");
const foodGrid = document.getElementById("food-grid");
const foodSpotlightContainer = document.getElementById("food-spotlight-container");
const foodResultsContainer = document.getElementById("food-results-container");
const foodEmptyState = document.getElementById("food-empty-state");
const foodStatLowest = document.getElementById("food-stat-lowest");
const foodStatAvg = document.getElementById("food-stat-avg");
const foodStatHighest = document.getElementById("food-stat-highest");
const foodStatTotal = document.getElementById("food-stat-total");
const foodCountBadge = document.getElementById("food-count-badge");
const foodGridTitle = document.getElementById("food-grid-title");

const DEFAULT_IMAGE_FALLBACK = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='64' height='64' fill='none' stroke='%238c734b' stroke-width='1.5'%3E%3Crect x='5' y='2' width='14' height='20' rx='2'/%3E%3Cline x1='12' y1='18' x2='12' y2='18.01' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E";

document.addEventListener("DOMContentLoaded", async () => {
    updateFavoritesBadge();
    await Promise.all([fetchStores(), fetchEvents(), fetchFoodDeals(), fetchGroceries()]);
    setupEventListeners();
    setupFoodEventListeners();
    setupGroceriesEventListeners();
    setupFavoritesEventListeners();
    setupCompareEventListeners();
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
    if (tabGroceries) {
        tabGroceries.addEventListener("click", () => switchView("groceries"));
    }
    if (tabFood) {
        tabFood.addEventListener("click", () => switchView("food"));
    }
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

    if (productLocationSelect) {
        productLocationSelect.addEventListener("change", (e) => {
            state.productLocation = e.target.value;
            updateProductPickupLabel(state.productLocation);
            if (searchInput.value.trim()) performSearch();
        });
    }

    if (toggleProductOnlyDiscounts) {
        toggleProductOnlyDiscounts.addEventListener("change", (e) => {
            state.productOnlyDiscounts = toggleProductOnlyDiscounts.checked;
            if (searchInput.value.trim()) performSearch();
        });
    }

    toggleAccessories.addEventListener("change", () => {
        if (searchInput.value.trim()) performSearch();
    });

    toggleRefurbished.addEventListener("change", () => {
        if (searchInput.value.trim()) performSearch();
    });

    if (toggleCajamarcaPickup) {
        toggleCajamarcaPickup.addEventListener("change", () => {
            state.pickupCajamarcaOnly = toggleCajamarcaPickup.checked;
            if (searchInput.value.trim()) performSearch();
        });
    }

    // Payment Filter Buttons
    document.querySelectorAll(".payment-filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".payment-filter-btn").forEach(b => {
                b.className = "payment-filter-btn px-2.5 py-1 rounded-md border text-xs font-medium transition bg-obsidian-950 border-obsidian-700 text-platinum-400 hover:text-gold-200 hover:border-gold-400/30";
            });
            btn.className = "payment-filter-btn px-2.5 py-1 rounded-md border text-xs font-medium transition active-pay-pill bg-obsidian-850 border-gold-400/50 text-gold-300 shadow-sm";
            state.paymentFilter = btn.dataset.pay;
            if (searchInput.value.trim()) performSearch();
        });
    });

    // Verdict Radar Filter Buttons
    document.querySelectorAll(".verdict-filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".verdict-filter-btn").forEach(b => {
                b.className = "verdict-filter-btn px-2.5 py-1 rounded-md border text-xs font-medium transition bg-obsidian-950 border-obsidian-700 text-platinum-400 hover:text-gold-200 hover:border-gold-400/30";
            });
            btn.className = "verdict-filter-btn px-2.5 py-1 rounded-md border text-xs font-medium transition active-verdict-pill bg-obsidian-850 border-gold-400/50 text-gold-300 shadow-sm";
            state.verdictFilter = btn.dataset.verdict;
            if (searchInput.value.trim()) performSearch();
        });
    });

    selectAllStoresBtn.addEventListener("click", () => {
        state.stores.forEach(s => state.selectedStores.add(s.id));
        renderStoreToggles();
        if (searchInput.value.trim()) performSearch();
    });

    exportCsvBtn.addEventListener("click", exportToCsv);

    // Initial label sync for locality
    if (state.productLocation) {
        updateProductPickupLabel(state.productLocation);
    }
}

function updateProductPickupLabel(loc) {
    if (!productPickupLabelText) return;
    if (loc === "cajamarca") {
        productPickupLabelText.textContent = "Retiro Gratis en Cajamarca";
        if (productPickupSubtext) productPickupSubtext.textContent = "(El Quinde / Real Plaza)";
    } else if (loc === "lima") {
        productPickupLabelText.textContent = "Retiro Gratis en Tienda";
        if (productPickupSubtext) productPickupSubtext.textContent = "(Lima Metropolitana)";
    } else if (loc === "arequipa") {
        productPickupLabelText.textContent = "Retiro Gratis en Arequipa";
        if (productPickupSubtext) productPickupSubtext.textContent = "(Mall Aventura / Cayma)";
    } else if (loc === "trujillo") {
        productPickupLabelText.textContent = "Retiro Gratis en Trujillo";
        if (productPickupSubtext) productPickupSubtext.textContent = "(Mallplaza / Real Plaza)";
    } else if (loc === "chiclayo_piura") {
        productPickupLabelText.textContent = "Retiro Gratis en Piura / Chiclayo";
        if (productPickupSubtext) productPickupSubtext.textContent = "(Mall Aventura / Real Plaza)";
    } else if (loc === "cusco") {
        productPickupLabelText.textContent = "Retiro Gratis en Cusco";
        if (productPickupSubtext) productPickupSubtext.textContent = "(Real Plaza Cusco)";
    } else {
        productPickupLabelText.textContent = "Solo retiro gratis en tienda";
        if (productPickupSubtext) productPickupSubtext.textContent = "(A nivel nacional)";
    }
}

function switchView(viewName) {
    state.activeView = viewName;
    const activeTab = "px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-lg transition text-gold-300 bg-obsidian-850 border border-gold-400/30 font-semibold shadow-sm flex items-center gap-1.5 whitespace-nowrap";
    const inactiveTab = "px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-lg transition text-platinum-400 hover:text-gold-200 hover:bg-obsidian-850 flex items-center gap-1.5 whitespace-nowrap";

    comparatorView.classList.add("hidden");
    if (groceriesView) groceriesView.classList.add("hidden");
    if (foodView) foodView.classList.add("hidden");
    eventsView.classList.add("hidden");

    tabComparator.className = inactiveTab;
    if (tabGroceries) tabGroceries.className = inactiveTab;
    if (tabFood) tabFood.className = inactiveTab;
    tabEvents.className = inactiveTab;

    if (viewName === "comparator") {
        comparatorView.classList.remove("hidden");
        tabComparator.className = activeTab;
    } else if (viewName === "groceries") {
        if (groceriesView) groceriesView.classList.remove("hidden");
        if (tabGroceries) tabGroceries.className = activeTab;
        if (!state.groceries || state.groceries.length === 0) fetchGroceries();
    } else if (viewName === "food") {
        if (foodView) foodView.classList.remove("hidden");
        if (tabFood) tabFood.className = activeTab;
    } else if (viewName === "events") {
        eventsView.classList.remove("hidden");
        tabEvents.className = activeTab;
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
    if (state.paymentFilter && state.paymentFilter !== "all") {
        params.append("payment", state.paymentFilter);
    }
    if (state.productLocation) {
        params.append("location", state.productLocation);
    }
    if (state.productOnlyDiscounts) {
        params.append("only_discounts", "true");
    }
    if (state.pickupCajamarcaOnly) {
        params.append("pickup_only", "true");
        if (state.productLocation === "cajamarca") {
            params.append("pickup_cajamarca", "true");
        }
    }

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
        const isFav = isFavorite(cheapest);
        const isCompared = state.compareItems.some(p => p.id === cheapest.id);

        bestDealContainer.innerHTML = `
            <div class="best-deal-luxury rounded-xl p-3.5 sm:p-5 flex flex-col sm:flex-row items-center sm:items-stretch gap-4 sm:gap-5 h-full relative">
                <!-- Favorite button on Spotlight -->
                <button type="button" class="spotlight-fav-btn absolute top-3 right-3 text-sm p-1.5 rounded-lg bg-obsidian-950/80 border border-obsidian-700/80 hover:border-gold-400/50 transition z-10" title="Guardar en favoritos">
                    <i class="${isFav ? 'fa-solid text-rose-500' : 'fa-regular text-platinum-400 hover:text-rose-400'} fa-heart"></i>
                </button>

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
                            ${cheapest.deal_verdict === "Mínimo Histórico" ? `
                                <span class="text-[9px] font-bold text-amber-300 bg-amber-950/80 border border-amber-500/50 px-1.5 py-0.5 rounded uppercase tracking-wider">
                                    🔥 Mínimo Histórico
                                </span>
                            ` : ''}
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

                        <!-- Retail nuances: Installments, Pickup & Payment -->
                        <div class="flex flex-wrap items-center justify-center sm:justify-start gap-x-3 gap-y-1 pt-1.5 text-[11px] text-platinum-400">
                            <span class="flex items-center gap-1 text-gold-300 font-medium">
                                <i class="fa-solid fa-credit-card text-[10px]"></i>
                                ${cheapest.installments_12x ? `12 cuotas de ${formatPrice(cheapest.installments_12x)} sin int.` : '12 cuotas sin int.'}
                            </span>
                            <span class="text-platinum-600">•</span>
                            <span class="flex items-center gap-1 ${cheapest.card_name ? 'text-purple-300 font-medium' : 'text-platinum-300'}">
                                ${cheapest.card_name ? `<i class="fa-solid fa-star text-purple-400 text-[10px]"></i> ${cheapest.card_name}` : `<i class="fa-solid fa-check text-emerald-400 text-[10px]"></i> Cualquier tarjeta/Yape`}
                            </span>
                            <span class="text-platinum-600">•</span>
                            <span class="flex items-center gap-1 ${cheapest.pickup_available ? 'text-emerald-300 font-medium' : 'text-platinum-400'}">
                                <i class="fa-solid ${cheapest.pickup_available ? 'fa-location-dot text-emerald-400' : 'fa-truck text-platinum-500'} text-[10px]"></i>
                                <span>${cheapest.pickup_location}</span>
                            </span>
                        </div>
                    </div>

                    <div class="pt-2 sm:pt-1.5 flex items-center gap-2">
                        <a 
                            href="${cheapest.url}" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            class="btn-gold flex-1 inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-xs uppercase tracking-wider shadow-md"
                        >
                            <span>Ir a la oferta en ${cheapest.store}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                        </a>
                        <button type="button" class="spotlight-compare-btn btn-platinum-outline px-3 py-2 rounded-lg text-xs font-medium flex items-center gap-1.5 whitespace-nowrap ${isCompared ? 'bg-gold-500/20 border-gold-400 text-gold-300' : ''}">
                            <i class="fa-solid ${isCompared ? 'fa-check text-gold-400' : 'fa-code-compare text-platinum-400'} text-[10px]"></i>
                            <span>${isCompared ? 'En comparativa' : 'Comparar'}</span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        const spotFavBtn = bestDealContainer.querySelector(".spotlight-fav-btn");
        if (spotFavBtn) spotFavBtn.addEventListener("click", () => toggleFavorite(cheapest));

        const spotCompBtn = bestDealContainer.querySelector(".spotlight-compare-btn");
        if (spotCompBtn) spotCompBtn.addEventListener("click", () => toggleCompareItem(cheapest));
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
        const isFav = isFavorite(prod);
        const isCompared = state.compareItems.some(p => p.id === prod.id);

        card.innerHTML = `
            <div>
                <!-- Top Info with Store, Condition & Favorite Heart -->
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
                        <button type="button" class="card-fav-btn text-xs p-1 text-platinum-500 hover:text-rose-400 transition" title="Favorito">
                            <i class="${isFav ? 'fa-solid text-rose-500' : 'fa-regular'} fa-heart"></i>
                        </button>
                    </div>
                </div>

                <!-- Product Thumbnail + Deal Radar Badge Overlay -->
                <div class="w-full h-32 xs:h-36 sm:h-40 bg-obsidian-950 rounded-lg p-2 sm:p-2.5 mb-2.5 sm:mb-3 flex items-center justify-center overflow-hidden border border-obsidian-700/50 relative">
                    <img 
                        src="${prod.image_url || DEFAULT_IMAGE_FALLBACK}" 
                        alt="${escapeHtml(prod.title)}"
                        class="max-w-full max-h-full object-contain"
                        onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'"
                    />
                    ${prod.deal_verdict === "Mínimo Histórico" ? `
                        <div class="absolute bottom-1.5 left-1.5 bg-amber-950/90 border border-amber-500/50 text-amber-300 text-[9px] font-bold px-1.5 py-0.2 rounded flex items-center gap-1 shadow">
                            <i class="fa-solid fa-fire text-amber-400"></i> Mínimo Histórico
                        </div>
                    ` : (prod.deal_verdict === "Buen Precio" ? `
                        <div class="absolute bottom-1.5 left-1.5 bg-emerald-950/90 border border-emerald-500/50 text-emerald-300 text-[9px] font-bold px-1.5 py-0.2 rounded flex items-center gap-1 shadow">
                            <i class="fa-solid fa-check text-emerald-400"></i> Buen Precio
                        </div>
                    ` : '')}
                </div>

                <!-- Title & Brand -->
                <div class="space-y-1">
                    <span class="text-[9px] sm:text-[10px] text-platinum-500 font-medium uppercase tracking-wider block">
                        ${prod.brand || 'Producto'}
                    </span>
                    <h3 class="text-xs font-medium text-platinum-200 line-clamp-2 leading-snug sm:leading-relaxed" title="${escapeHtml(prod.title)}">
                        ${escapeHtml(prod.title)}
                    </h3>
                </div>

                <!-- Logistics & Payment Highlights -->
                <div class="pt-2 space-y-1 text-[10px]">
                    <!-- Payment method -->
                    <div class="flex items-center gap-1 ${prod.card_name ? 'text-purple-300 font-medium' : 'text-platinum-400'} truncate">
                        <i class="fa-solid fa-credit-card text-[9px] ${prod.card_name ? 'text-purple-400' : 'text-emerald-400'} flex-shrink-0"></i>
                        <span class="truncate">${prod.payment_method}</span>
                    </div>

                    <!-- Store pickup / Courier -->
                    <div class="flex items-center gap-1 ${prod.pickup_available ? 'text-emerald-400 font-medium' : 'text-platinum-500'} truncate">
                        <i class="fa-solid ${prod.pickup_available ? 'fa-location-dot text-emerald-400' : 'fa-truck text-platinum-600'} text-[9px] flex-shrink-0"></i>
                        <span class="truncate">${prod.pickup_location}</span>
                    </div>

                    <!-- Installments -->
                    ${prod.installments_12x ? `
                        <div class="text-[9px] text-gold-400/90 font-mono">
                            12 cuotas de ${formatPrice(prod.installments_12x)} sin int.
                        </div>
                    ` : ''}
                </div>
            </div>

            <!-- Price & Actions -->
            <div class="pt-2.5 sm:pt-3 border-t border-obsidian-700/60 mt-2.5 sm:mt-3 space-y-2">
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

                <div class="flex items-center gap-1.5">
                    <a 
                        href="${prod.url}" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="btn-platinum-outline flex-1 flex items-center justify-center gap-1.5 text-xs font-medium py-1.5 sm:py-2 rounded-lg"
                    >
                        <span>Ver oferta</span>
                        <i class="fa-solid fa-arrow-up-right-from-square text-[9px] text-platinum-400"></i>
                    </a>
                    <button type="button" class="card-compare-btn px-2.5 py-1.5 sm:py-2 rounded-lg border text-xs font-medium transition flex items-center gap-1 ${isCompared ? 'bg-gold-500/20 border-gold-400 text-gold-300 font-bold' : 'bg-obsidian-950 border-obsidian-700 text-platinum-400 hover:text-white hover:border-gold-400/40'}" title="Comparar producto">
                        <i class="fa-solid ${isCompared ? 'fa-check text-gold-400' : 'fa-code-compare text-platinum-500'} text-[10px]"></i>
                    </button>
                </div>
            </div>
        `;

        const favBtn = card.querySelector(".card-fav-btn");
        if (favBtn) favBtn.addEventListener("click", () => toggleFavorite(prod));

        const compBtn = card.querySelector(".card-compare-btn");
        if (compBtn) compBtn.addEventListener("click", () => toggleCompareItem(prod));

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

// =========================================================
// FOOD DEALS, RAPPI & YAPE PROMOS SECTION
// =========================================================

async function fetchFoodDeals() {
    try {
        const params = new URLSearchParams();
        if (state.foodCategory && state.foodCategory !== "todas") {
            params.append("category", state.foodCategory);
        }
        if (state.foodPlatform && state.foodPlatform !== "todas") {
            params.append("platform", state.foodPlatform);
        }
        if (state.foodLocation && state.foodLocation !== "todas") {
            params.append("location", state.foodLocation);
        }
        if (state.foodOnlyDiscounts) {
            params.append("only_discounts", "true");
        }
        if (state.foodQuery && state.foodQuery.trim()) {
            params.append("q", state.foodQuery.trim());
        }
        params.append("sort", state.foodSort || "asc");

        const resp = await fetch(`/api/food-deals?${params.toString()}`);
        if (!resp.ok) throw new Error("Failed to fetch food deals");
        const data = await resp.json();

        state.foodDeals = data.results || [];
        state.foodStats = data.stats || {};
        state.foodCategories = data.categories || {};

        updateFoodCategoryBadges();
        renderFoodDeals();
    } catch (err) {
        console.error("Error fetching food deals:", err);
    }
}

function updateFoodCategoryBadges() {
    let totalAll = 0;
    const catKeys = ["pizza", "burger", "pollo", "makis", "chifa", "postres"];
    
    catKeys.forEach(cat => {
        const count = state.foodCategories[cat] || 0;
        totalAll += count;
        const el = document.getElementById(`cat-count-${cat}`);
        if (el) el.textContent = count;
    });

    const totalEl = document.getElementById("cat-count-todas");
    if (totalEl) totalEl.textContent = totalAll;
}

function renderFoodDeals() {
    if (!foodGrid) return;

    if (!state.foodDeals || state.foodDeals.length === 0) {
        if (foodResultsContainer) foodResultsContainer.classList.add("hidden");
        if (foodEmptyState) foodEmptyState.classList.remove("hidden");
        return;
    }

    if (foodResultsContainer) foodResultsContainer.classList.remove("hidden");
    if (foodEmptyState) foodEmptyState.classList.add("hidden");

    // 1. Stats updates
    if (foodStatLowest) foodStatLowest.textContent = formatPrice(state.foodStats.lowest_price);
    if (foodStatAvg) foodStatAvg.textContent = formatPrice(state.foodStats.average_price);
    if (foodStatHighest) foodStatHighest.textContent = formatPrice(state.foodStats.highest_price);
    if (foodStatTotal) foodStatTotal.textContent = String(state.foodStats.total_results);
    if (foodCountBadge) {
        const locLabel = (foodLocationSelect && foodLocationSelect.selectedOptions[0]) 
            ? foodLocationSelect.selectedOptions[0].text 
            : "Nacional";
        foodCountBadge.textContent = `${state.foodDeals.length} opciones (${locLabel.split('(')[0].trim()})`;
    }

    // 2. Spotlight Best Food Deal Card
    const cheapest = state.foodStats.cheapest_item || state.foodDeals[0];
    if (foodSpotlightContainer && cheapest) {
        const hasCoupon = Boolean(cheapest.coupon_code);
        const isRappi = cheapest.platform.includes("Rappi");
        const isYape = cheapest.platform.includes("Yape");
        const actionText = isRappi ? "Pedir en Rappi" : (isYape ? "Aprovechar en Yape" : `Ver en ${cheapest.brand}`);

        let platBadgeStyle = 'bg-obsidian-850 text-platinum-300 border-obsidian-700';
        if (isRappi) platBadgeStyle = 'bg-[#ff441f]/20 text-[#ff7051] border-[#ff441f]/40 font-semibold';
        else if (isYape) platBadgeStyle = 'bg-purple-950/80 text-purple-200 border-purple-500/40';

        foodSpotlightContainer.innerHTML = `
            <div class="best-deal-luxury rounded-xl p-3.5 sm:p-5 flex flex-col sm:flex-row items-center sm:items-stretch gap-4 sm:gap-5 h-full">
                <a href="${cheapest.deal_url}" target="_blank" rel="noopener noreferrer" class="w-28 h-28 xs:w-32 xs:h-32 sm:w-40 sm:h-40 flex-shrink-0 bg-obsidian-950 rounded-lg p-1.5 border border-gold-400/30 overflow-hidden flex items-center justify-center group cursor-pointer block" title="Abrir ${escapeHtml(cheapest.title)} en ${escapeHtml(cheapest.brand)}">
                    <img 
                        src="${cheapest.image_url || DEFAULT_IMAGE_FALLBACK}" 
                        alt="${escapeHtml(cheapest.title)}"
                        class="w-full h-full object-cover rounded-md transition-transform duration-300 group-hover:scale-105"
                        onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'"
                    />
                </a>

                <div class="flex-1 space-y-2 text-center sm:text-left flex flex-col justify-between w-full">
                    <div>
                        <div class="flex flex-wrap items-center justify-center sm:justify-start gap-1.5 sm:gap-2">
                            <span class="text-[9px] sm:text-[10px] font-semibold text-gold-300 bg-gold-900/60 border border-gold-400/40 px-2 py-0.5 rounded uppercase tracking-wider">
                                Mejor Precio
                            </span>
                            <span class="text-[10px] sm:text-[11px] px-2 py-0.5 rounded border flex items-center gap-1.5 ${platBadgeStyle}">
                                <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${cheapest.platform_color}"></span>
                                ${cheapest.platform}
                            </span>
                            <span class="text-[10px] sm:text-[11px] font-medium text-platinum-300 bg-obsidian-850 border border-obsidian-700 px-2 py-0.5 rounded">
                                ${cheapest.brand}
                            </span>
                            <span class="text-[10px] text-platinum-400 bg-obsidian-950 border border-obsidian-700 px-2 py-0.5 rounded flex items-center gap-1">
                                <i class="fa-solid fa-location-dot text-gold-400 text-[9px]"></i>
                                ${cheapest.location}
                            </span>
                        </div>

                        <a href="${cheapest.deal_url}" target="_blank" rel="noopener noreferrer" class="group block mt-1.5">
                            <h2 class="text-sm sm:text-base lg:text-lg font-semibold text-white group-hover:text-gold-300 transition leading-snug">
                                ${escapeHtml(cheapest.title)}
                            </h2>
                        </a>

                        <p class="text-xs text-platinum-400 line-clamp-2 mt-1 leading-relaxed">
                            ${escapeHtml(cheapest.description)}
                        </p>

                        <div class="flex flex-wrap items-baseline justify-center sm:justify-start gap-2 pt-2">
                            <span class="text-xl sm:text-2xl font-bold text-gold-300">
                                ${formatPrice(cheapest.price)}
                            </span>
                            ${cheapest.original_price ? `
                                <span class="text-xs text-platinum-500 line-through">
                                    ${formatPrice(cheapest.original_price)}
                                </span>
                            ` : ''}
                            ${cheapest.discount_percent ? `
                                <span class="text-xs text-gold-400 font-semibold bg-gold-900/40 border border-gold-400/30 px-1.5 py-0.5 rounded">
                                    -${cheapest.discount_percent}% de descuento
                                </span>
                            ` : `
                                <span class="text-[10px] text-platinum-400 bg-obsidian-950 border border-obsidian-700 px-1.5 py-0.5 rounded">
                                    Carta Regular
                                </span>
                            `}
                            <span class="text-[10px] text-platinum-500 flex items-center gap-1">
                                <i class="fa-regular fa-clock text-gold-400/80 text-[9px]"></i>
                                ${cheapest.delivery_time}
                            </span>
                        </div>
                    </div>

                    <!-- Action buttons -->
                    <div class="pt-2 sm:pt-1.5 flex flex-wrap items-center gap-2">
                        ${hasCoupon ? `
                            <button 
                                type="button" 
                                onclick="copyCouponToClipboard('${cheapest.coupon_code}', this)"
                                class="btn-platinum-outline px-3 py-2 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition text-gold-300 border-gold-400/40 hover:bg-gold-900/30"
                                title="Copiar cupón"
                            >
                                <i class="fa-regular fa-copy text-[11px]"></i>
                                <span>Cupón: <strong class="font-mono text-white">${cheapest.coupon_code}</strong></span>
                            </button>
                        ` : ''}
                        <a 
                            href="${cheapest.deal_url}" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            class="btn-gold px-4 py-2 rounded-lg text-xs uppercase tracking-wider inline-flex items-center justify-center gap-2 shadow-md flex-1 sm:flex-initial"
                        >
                            <span>${actionText}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    // 3. Render Food Cards Grid (Ranked lowest to highest)
    foodGrid.innerHTML = "";
    state.foodDeals.forEach((deal, index) => {
        const card = document.createElement("div");
        card.className = "luxury-card rounded-xl p-3 sm:p-4 flex flex-col justify-between";

        const isRank1 = (index === 0 && (state.foodSort || "asc") === "asc");
        const hasCoupon = Boolean(deal.coupon_code);
        const isRappi = deal.platform.includes("Rappi");
        const isYape = deal.platform.includes("Yape");
        const isPedidosYa = deal.platform.includes("PedidosYa");
        const btnText = isRappi 
            ? "Ver plato en Rappi" 
            : (isPedidosYa 
                ? "Pedir en PedidosYa" 
                : (isYape ? `Ver promo en ${deal.brand}` : `Ver plato en ${deal.brand}`));

        let platBadgeClass = "bg-obsidian-950 text-platinum-400 border border-obsidian-700/60";
        if (isRappi) platBadgeClass = "bg-[#ff441f]/20 text-[#ff7051] border border-[#ff441f]/40 font-semibold";
        else if (isYape) platBadgeClass = "bg-purple-950/80 text-purple-300 border border-purple-500/40";
        else if (isPedidosYa) platBadgeClass = "bg-[#ea1d2c]/20 text-[#ea1d2c] border border-[#ea1d2c]/40 font-semibold";

        card.innerHTML = `
            <div>
                <!-- Top Brand & Platform Info -->
                <div class="flex items-center justify-between gap-1.5 mb-2 sm:mb-2.5">
                    <div class="flex items-center gap-1.5 text-[10px] sm:text-[11px] font-medium text-platinum-300 truncate">
                        <span class="w-1.5 h-1.5 rounded-full flex-shrink-0" style="background-color: ${deal.platform_color || '#c5a880'}"></span>
                        <span class="truncate font-semibold">${escapeHtml(deal.brand)}</span>
                    </div>
                    <div class="flex items-center gap-1 sm:gap-1.5 text-[10px] sm:text-[11px] flex-shrink-0">
                        ${isRank1 ? `
                            <span class="text-gold-300 font-semibold text-[9px] sm:text-[10px] bg-gold-900/60 border border-gold-400/40 px-1.5 py-0.2 rounded uppercase tracking-wider">
                                Más Económico
                            </span>
                        ` : `
                            <span class="text-platinum-500 font-medium text-[10px]">#${index + 1}</span>
                        `}
                        <span class="text-[9px] sm:text-[10px] px-1.5 py-0.2 rounded font-medium ${platBadgeClass}">
                            ${deal.platform}
                        </span>
                    </div>
                </div>

                <!-- Food Image Thumbnail (Clickable directly to product) -->
                <a href="${deal.deal_url}" target="_blank" rel="noopener noreferrer" class="block w-full h-32 xs:h-36 sm:h-40 bg-obsidian-950 rounded-lg mb-2 sm:mb-2.5 overflow-hidden border border-obsidian-700/50 relative group cursor-pointer" title="Abrir ${escapeHtml(deal.title)} en ${escapeHtml(deal.brand)}">
                    <img 
                        src="${deal.image_url || DEFAULT_IMAGE_FALLBACK}" 
                        alt="${escapeHtml(deal.title)}"
                        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                        onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'"
                    />
                    <div class="absolute top-2 left-2 flex flex-col gap-1">
                        <span class="text-[9px] font-medium px-2 py-0.5 rounded-md bg-obsidian-950/85 backdrop-blur-sm border border-obsidian-700 text-platinum-300">
                            ${escapeHtml(deal.category_name)}
                        </span>
                    </div>
                    <div class="absolute bottom-2 right-2">
                        <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-obsidian-950/90 text-platinum-400 border border-obsidian-700/80">
                            ${deal.delivery_time}
                        </span>
                    </div>
                    <div class="absolute inset-0 bg-gold-400/5 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <span class="bg-obsidian-950/90 border border-gold-400/50 text-gold-300 text-[10px] font-semibold px-2 py-1 rounded shadow-lg flex items-center gap-1">
                            <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i> Ver producto
                        </span>
                    </div>
                </a>

                <!-- Location tag -->
                <div class="flex items-center gap-1 text-[10px] text-platinum-500 mb-1.5 truncate">
                    <i class="fa-solid fa-location-dot text-gold-400 text-[9px] flex-shrink-0"></i>
                    <span class="truncate">${deal.location}</span>
                </div>

                <!-- Title & Description (Clickable title directly to product) -->
                <div class="space-y-1">
                    <a href="${deal.deal_url}" target="_blank" rel="noopener noreferrer" class="block group">
                        <h3 class="text-xs sm:text-sm font-semibold text-platinum-100 group-hover:text-gold-300 transition line-clamp-2 leading-snug" title="${escapeHtml(deal.title)}">
                            ${escapeHtml(deal.title)}
                        </h3>
                    </a>
                    <p class="text-[11px] text-platinum-400 line-clamp-2 leading-relaxed">
                        ${escapeHtml(deal.description)}
                    </p>
                </div>
            </div>

            <!-- Price, Coupon & Action Button -->
            <div class="pt-2.5 sm:pt-3 border-t border-obsidian-700/60 mt-2.5 sm:mt-3 space-y-2.5">
                <!-- Price row -->
                <div class="flex items-baseline justify-between gap-1">
                    <div>
                        <div class="text-base sm:text-lg font-bold ${isRank1 ? 'text-gold-300' : 'text-white'}">
                            ${formatPrice(deal.price)}
                        </div>
                        ${deal.original_price ? `
                            <div class="text-[10px] sm:text-[11px] text-platinum-500 line-through">
                                ${formatPrice(deal.original_price)}
                            </div>
                        ` : ''}
                    </div>

                    ${deal.discount_percent ? `
                        <span class="text-[9px] sm:text-[10px] font-semibold text-gold-300 bg-gold-900/40 border border-gold-400/30 px-1.5 py-0.5 rounded">
                            -${deal.discount_percent}%
                        </span>
                    ` : `
                        <span class="text-[9px] text-platinum-500 bg-obsidian-950 border border-obsidian-700/70 px-1.5 py-0.5 rounded">
                            Carta regular
                        </span>
                    `}
                </div>

                <!-- Coupon Code if available -->
                ${hasCoupon ? `
                    <div class="bg-obsidian-950 border border-gold-400/25 rounded-lg px-2.5 py-1.5 flex items-center justify-between gap-2">
                        <div class="flex items-center gap-1.5 text-[11px] text-platinum-400 truncate">
                            <i class="fa-solid fa-ticket text-gold-400 text-[10px] flex-shrink-0"></i>
                            <span class="font-mono text-gold-200 font-bold truncate">${deal.coupon_code}</span>
                        </div>
                        <button 
                            type="button" 
                            onclick="copyCouponToClipboard('${deal.coupon_code}', this)"
                            class="text-[10px] text-gold-400 hover:text-gold-200 px-1.5 py-0.5 rounded bg-gold-900/40 border border-gold-400/30 transition flex items-center gap-1 flex-shrink-0"
                            title="Copiar cupón"
                        >
                            <i class="fa-regular fa-copy text-[9px]"></i>
                            <span>Copiar</span>
                        </button>
                    </div>
                ` : `
                    <div class="text-[10px] text-platinum-500 flex items-center gap-1.5 py-0.5">
                        <i class="fa-regular fa-clock text-[9px]"></i>
                        <span>${deal.expiration}</span>
                    </div>
                `}

                <!-- Button -->
                <a 
                    href="${deal.deal_url}" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="${isRappi ? 'bg-[#ff441f]/20 hover:bg-[#ff441f]/30 border border-[#ff441f]/40 text-[#ff7051]' : 'btn-platinum-outline'} w-full flex items-center justify-center gap-1.5 text-xs font-medium py-1.5 sm:py-2 rounded-lg transition"
                >
                    <span>${btnText}</span>
                    <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
            </div>
        `;

        foodGrid.appendChild(card);
    });
}

function setupFoodEventListeners() {
    // 1. Food Category Buttons
    const categoryButtons = document.querySelectorAll(".food-cat-btn");
    categoryButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const cat = btn.dataset.category;
            state.foodCategory = cat;

            categoryButtons.forEach(b => {
                b.className = "food-cat-btn px-3 py-1.5 rounded-lg border text-xs font-medium transition flex items-center gap-1.5 bg-obsidian-950 border-obsidian-700/80 text-platinum-400 hover:text-gold-200 hover:border-gold-400/30";
            });
            btn.className = "food-cat-btn px-3 py-1.5 rounded-lg border text-xs font-medium transition flex items-center gap-1.5 active-food-cat bg-obsidian-850 border-gold-400/50 text-gold-300 shadow-sm";

            fetchFoodDeals();
        });
    });

    // 2. Food Platform Buttons
    const platformButtons = document.querySelectorAll(".food-platform-btn");
    platformButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const plat = btn.dataset.platform;
            state.foodPlatform = plat;

            platformButtons.forEach(b => {
                b.className = "food-platform-btn px-2.5 py-1 rounded-md border text-xs font-medium transition bg-obsidian-950 border-obsidian-700/70 text-platinum-400 hover:text-gold-300 hover:border-gold-500/40 flex items-center gap-1.5";
            });
            btn.className = "food-platform-btn px-2.5 py-1 rounded-md border text-xs font-medium transition active-food-plat bg-obsidian-850 border-gold-400/40 text-gold-300 flex items-center gap-1.5";

            fetchFoodDeals();
        });
    });

    // 3. Localidad / Distrito Select
    if (foodLocationSelect) {
        foodLocationSelect.addEventListener("change", (e) => {
            state.foodLocation = e.target.value;
            fetchFoodDeals();
        });
    }

    // 4. Toggle Solo Ofertas vs Carta Completa
    if (toggleFoodOnlyDiscounts) {
        toggleFoodOnlyDiscounts.addEventListener("change", (e) => {
            state.foodOnlyDiscounts = e.target.checked;
            fetchFoodDeals();
        });
    }

    // 5. Food Search Input
    let searchDebounceTimer;
    if (foodSearchInput) {
        foodSearchInput.addEventListener("input", () => {
            const val = foodSearchInput.value.trim();
            if (foodClearBtn) {
                if (val.length > 0) foodClearBtn.classList.remove("hidden");
                else foodClearBtn.classList.add("hidden");
            }
            clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(() => {
                state.foodQuery = val;
                fetchFoodDeals();
            }, 300);
        });
    }

    if (foodClearBtn) {
        foodClearBtn.addEventListener("click", () => {
            if (foodSearchInput) {
                foodSearchInput.value = "";
                foodClearBtn.classList.add("hidden");
                state.foodQuery = "";
                fetchFoodDeals();
                foodSearchInput.focus();
            }
        });
    }

    // 6. Food Sort Select
    if (foodSortSelect) {
        foodSortSelect.addEventListener("change", (e) => {
            state.foodSort = e.target.value;
            fetchFoodDeals();
        });
    }
}

// Global helper for coupon copying
window.copyCouponToClipboard = function(code, btn) {
    if (!code) return;
    const originalHtml = btn.innerHTML;

    const onSuccess = () => {
        btn.innerHTML = `<i class="fa-solid fa-check text-emerald-400 text-[10px]"></i> <span class="text-emerald-400 font-bold">¡Copiado!</span>`;
        setTimeout(() => {
            btn.innerHTML = originalHtml;
        }, 2000);
    };

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(code).then(onSuccess).catch(() => {
            fallbackCopy(code, onSuccess);
        });
    } else {
        fallbackCopy(code, onSuccess);
    }
};

function fallbackCopy(text, cb) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
        if (cb) cb();
    } catch (err) {
        console.error('Fallback copy error:', err);
    }
    document.body.removeChild(textArea);
}

// =========================================================
// FAVORITES / WISHLIST SYSTEM
// =========================================================

function getFavoriteKey(item) {
    if (item.fav_id) return item.fav_id;
    if (item.id) return item.id;
    const store = item.store || item.platform || item.brand || 'item';
    const title = item.title || item.name || '';
    return `${store}_${title}`.toLowerCase().replace(/[^a-z0-9]/g, '_');
}

function isFavorite(item) {
    const key = getFavoriteKey(item);
    return state.favorites.some(f => f.fav_id === key);
}

function toggleFavorite(item) {
    const key = getFavoriteKey(item);
    const existingIndex = state.favorites.findIndex(f => f.fav_id === key);

    if (existingIndex >= 0) {
        state.favorites.splice(existingIndex, 1);
    } else {
        state.favorites.unshift({
            fav_id: key,
            id: item.id || key,
            title: item.title || item.name,
            store: item.store || item.platform || item.brand || 'Tienda',
            store_color: item.store_color || item.platform_color || item.color || '#c5a880',
            price: item.price != null ? item.price : (item.lowest_price != null ? item.lowest_price : 0),
            original_price: item.original_price || null,
            discount_percent: item.discount_percent || null,
            url: item.url || item.deal_url || (item.prices && item.prices[0] ? item.prices[0].url : '#'),
            image_url: item.image_url,
            pickup_location: item.pickup_location || (item.pickup_cajamarca ? 'Cajamarca' : 'Envío'),
            deal_verdict: item.deal_verdict || null
        });
    }

    saveFavoritesToStorage();
    updateFavoritesBadge();
    renderFavoritesList();

    // Refresh active view to toggle heart icon
    if (state.activeView === "comparator") renderResults();
    else if (state.activeView === "groceries") renderGroceries();
    else if (state.activeView === "food") renderFoodDeals();
}

function updateFavoritesBadge() {
    const count = state.favorites.length;
    if (favCountBadge) favCountBadge.textContent = count;
    if (favModalCounter) favModalCounter.textContent = count;
}

function renderFavoritesList() {
    if (!favoritesList) return;

    if (state.favorites.length === 0) {
        favoritesList.innerHTML = `
            <div class="py-12 text-center space-y-2">
                <i class="fa-regular fa-heart text-platinum-600 text-3xl block"></i>
                <p class="text-sm font-semibold text-platinum-300">No tienes productos en favoritos</p>
                <p class="text-xs text-platinum-500">Toca el ícono de corazón en cualquier producto o promo para guardarlo aquí.</p>
            </div>
        `;
        return;
    }

    favoritesList.innerHTML = "";
    state.favorites.forEach((fav, index) => {
        const itemRow = document.createElement("div");
        itemRow.className = "flex items-center justify-between gap-3 p-3 rounded-xl bg-obsidian-900 border border-obsidian-800 hover:border-gold-400/30 transition";

        itemRow.innerHTML = `
            <div class="flex items-center gap-3 min-w-0">
                <div class="w-12 h-12 rounded-lg bg-obsidian-950 border border-obsidian-700/60 p-1 flex items-center justify-center flex-shrink-0">
                    <img src="${fav.image_url || DEFAULT_IMAGE_FALLBACK}" alt="${escapeHtml(fav.title)}" class="max-w-full max-h-full object-contain" onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'">
                </div>
                <div class="space-y-0.5 min-w-0">
                    <div class="flex items-center gap-1.5 text-[10px]">
                        <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${fav.store_color}"></span>
                        <span class="font-medium text-platinum-300">${fav.store}</span>
                        ${fav.deal_verdict ? `<span class="text-amber-400 font-bold">• ${fav.deal_verdict}</span>` : ''}
                    </div>
                    <h4 class="text-xs font-semibold text-white truncate max-w-sm" title="${escapeHtml(fav.title)}">${escapeHtml(fav.title)}</h4>
                    <div class="flex items-baseline gap-2">
                        <span class="text-xs sm:text-sm font-bold text-gold-300">${formatPrice(fav.price)}</span>
                        ${fav.original_price ? `<span class="text-[10px] text-platinum-500 line-through">${formatPrice(fav.original_price)}</span>` : ''}
                    </div>
                </div>
            </div>

            <div class="flex items-center gap-2 flex-shrink-0">
                <a href="${fav.url}" target="_blank" rel="noopener noreferrer" class="btn-gold px-3 py-1.5 rounded-lg text-[11px] font-semibold flex items-center gap-1">
                    <span>Comprar</span>
                    <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                </a>
                <button type="button" class="remove-fav-btn text-platinum-500 hover:text-rose-400 p-1.5 transition text-xs" data-index="${index}" title="Quitar de favoritos">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </div>
        `;

        const removeBtn = itemRow.querySelector(".remove-fav-btn");
        removeBtn.addEventListener("click", () => {
            state.favorites.splice(index, 1);
            saveFavoritesToStorage();
            updateFavoritesBadge();
            renderFavoritesList();
            if (state.activeView === "comparator") renderResults();
            else if (state.activeView === "groceries") renderGroceries();
            else if (state.activeView === "food") renderFoodDeals();
        });

        favoritesList.appendChild(itemRow);
    });
}

function setupFavoritesEventListeners() {
    if (openFavoritesBtn) {
        openFavoritesBtn.addEventListener("click", () => {
            renderFavoritesList();
            if (favoritesModal) favoritesModal.classList.remove("hidden");
        });
    }

    const closeFavorites = () => {
        if (favoritesModal) favoritesModal.classList.add("hidden");
    };

    if (closeFavoritesModal) closeFavoritesModal.addEventListener("click", closeFavorites);
    if (closeFavoritesBtnFooter) closeFavoritesBtnFooter.addEventListener("click", closeFavorites);

    if (favoritesModal) {
        favoritesModal.addEventListener("click", (e) => {
            if (e.target === favoritesModal) closeFavorites();
        });
    }

    if (clearAllFavoritesBtn) {
        clearAllFavoritesBtn.addEventListener("click", () => {
            if (state.favorites.length === 0) return;
            state.favorites = [];
            saveFavoritesToStorage();
            updateFavoritesBadge();
            renderFavoritesList();
            if (state.activeView === "comparator") renderResults();
            else if (state.activeView === "groceries") renderGroceries();
            else if (state.activeView === "food") renderFoodDeals();
        });
    }
}

// =========================================================
// SIDE-BY-SIDE COMPARISON SYSTEM
// =========================================================

function toggleCompareItem(prod) {
    const idx = state.compareItems.findIndex(p => p.id === prod.id);
    if (idx >= 0) {
        state.compareItems.splice(idx, 1);
    } else {
        if (state.compareItems.length >= 2) {
            state.compareItems.shift(); // remove oldest to keep 2
        }
        state.compareItems.push(prod);
    }

    updateCompareTray();
    renderResults();
}

function updateCompareTray() {
    if (!compareTray) return;
    const count = state.compareItems.length;

    if (count === 0) {
        compareTray.classList.add("translate-y-32", "opacity-0", "pointer-events-none");
        return;
    }

    compareTray.classList.remove("translate-y-32", "opacity-0", "pointer-events-none");

    if (compareTrayPreviews) {
        compareTrayPreviews.innerHTML = state.compareItems.map(p => `
            <div class="w-8 h-8 rounded-full border-2 border-gold-400 bg-obsidian-950 overflow-hidden flex items-center justify-center shadow">
                <img src="${p.image_url || DEFAULT_IMAGE_FALLBACK}" alt="${escapeHtml(p.title)}" class="max-w-full max-h-full object-contain p-0.5" onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'">
            </div>
        `).join('');
    }

    if (compareTrayText) {
        compareTrayText.textContent = count === 1 
            ? "1 de 2 seleccionados (elige otro para comparar)" 
            : "¡2 de 2 listos para comparar!";
    }

    if (compareTrayBtn) {
        compareTrayBtn.disabled = (count < 2);
        compareTrayBtn.className = count === 2
            ? "btn-gold px-3.5 sm:px-4 py-1.5 rounded-lg text-xs uppercase tracking-wider font-semibold flex items-center gap-1.5 whitespace-nowrap shadow-md cursor-pointer"
            : "bg-obsidian-800 text-platinum-500 border border-obsidian-700 px-3.5 sm:px-4 py-1.5 rounded-lg text-xs uppercase tracking-wider font-semibold flex items-center gap-1.5 whitespace-nowrap cursor-not-allowed";
    }
}

function openCompareModal() {
    if (state.compareItems.length < 2 || !compareModalContent) return;
    const [p1, p2] = state.compareItems;
    const diff = Math.abs(p1.price - p2.price);
    const p1Cheaper = p1.price < p2.price;
    const p2Cheaper = p2.price < p1.price;

    compareModalContent.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
            <!-- Product 1 Card -->
            <div class="luxury-card rounded-xl p-4 sm:p-5 flex flex-col justify-between space-y-4 ${p1Cheaper ? 'border-gold-400/50 shadow-lg shadow-gold-500/10' : ''}">
                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[10px] font-semibold text-platinum-300 bg-obsidian-850 border border-obsidian-700 px-2 py-0.5 rounded flex items-center gap-1.5">
                            <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${p1.store_color}"></span>
                            ${p1.store}
                        </span>
                        ${p1Cheaper ? '<span class="text-[10px] font-bold text-gold-300 bg-gold-900/60 border border-gold-400/40 px-2 py-0.5 rounded">MÁS ECONÓMICO</span>' : ''}
                    </div>

                    <div class="w-full h-36 sm:h-44 bg-obsidian-950 rounded-lg p-2 flex items-center justify-center border border-obsidian-700/50">
                        <img src="${p1.image_url || DEFAULT_IMAGE_FALLBACK}" alt="${escapeHtml(p1.title)}" class="max-w-full max-h-full object-contain" onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'">
                    </div>

                    <h4 class="text-xs sm:text-sm font-semibold text-white leading-snug line-clamp-2">${escapeHtml(p1.title)}</h4>

                    <div class="space-y-1">
                        <div class="text-xl sm:text-2xl font-bold text-gold-300">${formatPrice(p1.price)}</div>
                        ${p1Cheaper && diff > 0 ? `<div class="text-xs text-emerald-400 font-medium">S/ ${diff.toLocaleString('es-PE', {minimumFractionDigits: 2})} de ahorro frente a ${p2.store}</div>` : ''}
                    </div>

                    <!-- Comparison Table Specs -->
                    <div class="bg-obsidian-950/80 rounded-lg p-2.5 sm:p-3 space-y-2 text-xs border border-obsidian-800">
                        <div class="flex justify-between text-platinum-400">
                            <span>Medio de Pago:</span>
                            <span class="text-white font-medium text-right">${p1.payment_method}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Retiro en Cajamarca:</span>
                            <span class="text-white font-medium text-right ${p1.pickup_cajamarca ? 'text-emerald-400' : ''}">${p1.pickup_location}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Cuotas sin intereses:</span>
                            <span class="text-gold-300 font-medium text-right">${p1.installments_12x ? `12x ${formatPrice(p1.installments_12x)}` : 'Sin cuotas'}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Almacenamiento:</span>
                            <span class="text-white font-medium text-right">${(p1.specs && p1.specs.Almacenamiento) || 'Estándar'}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Memoria RAM:</span>
                            <span class="text-white font-medium text-right">${(p1.specs && p1.specs["Memoria RAM"]) || 'Estándar'}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Pantalla:</span>
                            <span class="text-white font-medium text-right">${(p1.specs && p1.specs.Pantalla) || 'Estándar'}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Garantía Oficial:</span>
                            <span class="text-white font-medium text-right">${(p1.specs && p1.specs.Garantía) || '12 Meses Oficial'}</span>
                        </div>
                    </div>
                </div>

                <a href="${p1.url}" target="_blank" rel="noopener noreferrer" class="btn-gold w-full text-center py-2.5 rounded-lg text-xs uppercase tracking-wider font-semibold">
                    Ir a la oferta en ${p1.store}
                </a>
            </div>

            <!-- Product 2 Card -->
            <div class="luxury-card rounded-xl p-4 sm:p-5 flex flex-col justify-between space-y-4 ${p2Cheaper ? 'border-gold-400/50 shadow-lg shadow-gold-500/10' : ''}">
                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[10px] font-semibold text-platinum-300 bg-obsidian-850 border border-obsidian-700 px-2 py-0.5 rounded flex items-center gap-1.5">
                            <span class="w-1.5 h-1.5 rounded-full" style="background-color: ${p2.store_color}"></span>
                            ${p2.store}
                        </span>
                        ${p2Cheaper ? '<span class="text-[10px] font-bold text-gold-300 bg-gold-900/60 border border-gold-400/40 px-2 py-0.5 rounded">MÁS ECONÓMICO</span>' : ''}
                    </div>

                    <div class="w-full h-36 sm:h-44 bg-obsidian-950 rounded-lg p-2 flex items-center justify-center border border-obsidian-700/50">
                        <img src="${p2.image_url || DEFAULT_IMAGE_FALLBACK}" alt="${escapeHtml(p2.title)}" class="max-w-full max-h-full object-contain" onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'">
                    </div>

                    <h4 class="text-xs sm:text-sm font-semibold text-white leading-snug line-clamp-2">${escapeHtml(p2.title)}</h4>

                    <div class="space-y-1">
                        <div class="text-xl sm:text-2xl font-bold text-gold-300">${formatPrice(p2.price)}</div>
                        ${p2Cheaper && diff > 0 ? `<div class="text-xs text-emerald-400 font-medium">S/ ${diff.toLocaleString('es-PE', {minimumFractionDigits: 2})} de ahorro frente a ${p1.store}</div>` : ''}
                    </div>

                    <!-- Comparison Table Specs -->
                    <div class="bg-obsidian-950/80 rounded-lg p-2.5 sm:p-3 space-y-2 text-xs border border-obsidian-800">
                        <div class="flex justify-between text-platinum-400">
                            <span>Medio de Pago:</span>
                            <span class="text-white font-medium text-right">${p2.payment_method}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Retiro en Cajamarca:</span>
                            <span class="text-white font-medium text-right ${p2.pickup_cajamarca ? 'text-emerald-400' : ''}">${p2.pickup_location}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Cuotas sin intereses:</span>
                            <span class="text-gold-300 font-medium text-right">${p2.installments_12x ? `12x ${formatPrice(p2.installments_12x)}` : 'Sin cuotas'}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Almacenamiento:</span>
                            <span class="text-white font-medium text-right">${(p2.specs && p2.specs.Almacenamiento) || 'No especificado'}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Memoria RAM:</span>
                            <span class="text-white font-medium text-right">${(p2.specs && p2.specs["Memoria RAM"]) || 'Estándar'}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Pantalla:</span>
                            <span class="text-white font-medium text-right">${(p2.specs && p2.specs.Pantalla) || 'Estándar'}</span>
                        </div>
                        <div class="flex justify-between text-platinum-400">
                            <span>Garantía Oficial:</span>
                            <span class="text-white font-medium text-right">${(p2.specs && p2.specs.Garantía) || '12 Meses Oficial'}</span>
                        </div>
                    </div>
                </div>

                <a href="${p2.url}" target="_blank" rel="noopener noreferrer" class="btn-gold w-full text-center py-2.5 rounded-lg text-xs uppercase tracking-wider font-semibold">
                    Ir a la oferta en ${p2.store}
                </a>
            </div>
        </div>
    `;

    if (compareModal) compareModal.classList.remove("hidden");
}

function setupCompareEventListeners() {
    if (compareTrayBtn) {
        compareTrayBtn.addEventListener("click", () => {
            if (state.compareItems.length === 2) openCompareModal();
        });
    }

    if (compareTrayClear) {
        compareTrayClear.addEventListener("click", () => {
            state.compareItems = [];
            updateCompareTray();
            renderResults();
        });
    }

    const closeCompare = () => {
        if (compareModal) compareModal.classList.add("hidden");
    };

    if (closeCompareModal) closeCompareModal.addEventListener("click", closeCompare);

    if (compareModal) {
        compareModal.addEventListener("click", (e) => {
            if (e.target === compareModal) closeCompare();
        });
    }
}

// =========================================================
// GROCERIES & SUPERMARKET PRICE COMPARATOR SYSTEM
// =========================================================

async function fetchGroceries() {
    try {
        const params = new URLSearchParams();
        if (state.groceriesCategory && state.groceriesCategory !== "todas") {
            params.append("category", state.groceriesCategory);
        }
        if (state.groceriesQuery && state.groceriesQuery.trim()) {
            params.append("q", state.groceriesQuery.trim());
        }
        params.append("sort", "asc");

        const resp = await fetch(`/api/groceries?${params.toString()}`);
        if (!resp.ok) throw new Error("Failed to fetch groceries");
        const data = await resp.json();

        state.groceries = data.results || [];
        state.groceriesStats = data.stats || {};
        renderGroceries();
    } catch (err) {
        console.error("Error fetching groceries:", err);
    }
}

function renderGroceries() {
    if (!groceriesGrid) return;

    // Update Totals
    if (basketTotalMetro) basketTotalMetro.textContent = formatPrice(state.groceriesStats.total_metro_basket);
    if (basketTotalTottus) basketTotalTottus.textContent = formatPrice(state.groceriesStats.total_tottus_basket);
    if (basketTotalPlazavea) basketTotalPlazavea.textContent = formatPrice(state.groceriesStats.total_plazavea_basket);
    if (basketMaxSaving) basketMaxSaving.textContent = `Ahorras ${formatPrice(state.groceriesStats.max_possible_saving)}`;
    if (groceriesCountBadge) groceriesCountBadge.textContent = `${state.groceries.length} productos`;

    groceriesGrid.innerHTML = "";

    state.groceries.forEach((item, index) => {
        const card = document.createElement("div");
        card.className = "luxury-card rounded-xl p-3.5 sm:p-4 flex flex-col justify-between space-y-3";

        const isFav = isFavorite(item);

        card.innerHTML = `
            <div>
                <!-- Top category & Favorite heart -->
                <div class="flex items-center justify-between gap-1.5 mb-2">
                    <span class="text-[9px] font-semibold text-emerald-300 bg-emerald-950/80 border border-emerald-500/40 px-2 py-0.5 rounded uppercase tracking-wider">
                        ${escapeHtml(item.category_label)}
                    </span>
                    <button type="button" class="groc-fav-btn text-xs p-1 text-platinum-500 hover:text-rose-400 transition" title="Guardar en favoritos">
                        <i class="${isFav ? 'fa-solid text-rose-500' : 'fa-regular'} fa-heart"></i>
                    </button>
                </div>

                <!-- Product Thumbnail -->
                <div class="w-full h-32 bg-obsidian-950 rounded-lg p-2 mb-2 flex items-center justify-center border border-obsidian-700/50">
                    <img src="${item.image_url || DEFAULT_IMAGE_FALLBACK}" alt="${escapeHtml(item.name)}" class="max-w-full max-h-full object-contain" onerror="this.src='${DEFAULT_IMAGE_FALLBACK}'">
                </div>

                <!-- Title & Unit -->
                <div class="space-y-0.5">
                    <span class="text-[10px] text-platinum-500 uppercase tracking-wider font-semibold block">${item.unit}</span>
                    <h3 class="text-xs sm:text-sm font-semibold text-platinum-100 line-clamp-2 leading-snug" title="${escapeHtml(item.name)}">
                        ${escapeHtml(item.name)}
                    </h3>
                </div>

                <!-- Supermarket Price Comparison Rows (Ranked lowest to highest) -->
                <div class="mt-3 space-y-1.5 pt-2 border-t border-obsidian-800">
                    <span class="text-[9px] uppercase tracking-wider text-platinum-500 font-semibold block">Precios por Supermercado:</span>
                    ${item.prices.map((p, idx) => {
                        const isCheapest = (idx === 0);
                        return `
                            <div class="flex items-center justify-between p-1.5 rounded-lg ${isCheapest ? 'bg-obsidian-900 border border-gold-400/40 shadow-sm' : 'bg-obsidian-950 border border-obsidian-800/80'} text-xs">
                                <div class="flex items-center gap-1.5 truncate">
                                    <span class="w-2 h-2 rounded-full" style="background-color: ${p.color}"></span>
                                    <span class="font-medium text-platinum-200 truncate">${p.store}</span>
                                    <span class="text-[9px] text-platinum-500 truncate hidden xs:inline">(${p.pickup_cajamarca})</span>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <span class="font-bold ${isCheapest ? 'text-gold-300' : 'text-platinum-300'}">${formatPrice(p.price)}</span>
                                    <a href="${p.url}" target="_blank" rel="noopener noreferrer" class="text-platinum-400 hover:text-gold-300 p-0.5 transition" title="Ver en ${p.store}">
                                        <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                                    </a>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>

            <!-- Best deal highlight footer -->
            <div class="pt-2 border-t border-obsidian-700/60 flex items-center justify-between text-xs">
                <span class="text-platinum-400 text-[11px]">
                    Mejor precio en <strong class="text-gold-300 font-semibold">${item.cheapest_store}</strong>
                </span>
                ${item.saving_amount > 0 ? `
                    <span class="text-emerald-400 font-semibold text-[10px] bg-emerald-950/60 border border-emerald-500/30 px-1.5 py-0.5 rounded">
                        Ahorras S/ ${item.saving_amount.toFixed(2)}
                    </span>
                ` : ''}
            </div>
        `;

        const favBtn = card.querySelector(".groc-fav-btn");
        if (favBtn) favBtn.addEventListener("click", () => toggleFavorite(item));

        groceriesGrid.appendChild(card);
    });
}

function setupGroceriesEventListeners() {
    // 1. Category Pills
    document.querySelectorAll(".grocery-cat-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".grocery-cat-btn").forEach(b => {
                b.className = "grocery-cat-btn px-3 py-1.5 rounded-lg border text-xs font-medium transition bg-obsidian-950 border-obsidian-700 text-platinum-400 hover:text-gold-200 hover:border-gold-400/30";
            });
            btn.className = "grocery-cat-btn px-3 py-1.5 rounded-lg border text-xs font-medium transition active-groc-cat bg-obsidian-850 border-gold-400/50 text-gold-300 shadow-sm";

            state.groceriesCategory = btn.dataset.category;
            fetchGroceries();
        });
    });

    // 2. Search Input
    let debounceTimer;
    if (groceriesSearchInput) {
        groceriesSearchInput.addEventListener("input", () => {
            const val = groceriesSearchInput.value.trim();
            if (groceriesClearBtn) {
                if (val.length > 0) groceriesClearBtn.classList.remove("hidden");
                else groceriesClearBtn.classList.add("hidden");
            }
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                state.groceriesQuery = val;
                fetchGroceries();
            }, 300);
        });
    }

    if (groceriesClearBtn) {
        groceriesClearBtn.addEventListener("click", () => {
            if (groceriesSearchInput) {
                groceriesSearchInput.value = "";
                groceriesClearBtn.classList.add("hidden");
                state.groceriesQuery = "";
                fetchGroceries();
                groceriesSearchInput.focus();
            }
        });
    }
}

