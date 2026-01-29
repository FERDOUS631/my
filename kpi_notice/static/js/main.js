
    let NOTICES = [];
let currentPage = 1;
const rowsPerPage = 10; 

let currentFilter = 'All';
let searchQuery = '';

const tableBody = document.getElementById('notice-table-body');
const searchInput = document.getElementById('notice-search');
const filterBtns = document.querySelectorAll('.filter-btn');
const noticeCountSpan = document.getElementById('notice-count');
const paginationWrapper = document.getElementById('pagination-wrapper');

// API Fetch
fetch('/api/notices/')
    .then(res => res.json())
    .then(data => {
        NOTICES = data.map(n => ({
            id: n.id,
            sl: n.sl,
            date: n.date,
            dept: n.department,
            subject: n.subject,
            author: n.author,
            description: n.description,
            pdf_file: n.pdf_file
        }));
        renderNotices();
    });

// Render function
function renderNotices() {
 
    const filtered = NOTICES.filter(n => {
        const matchDept = currentFilter === 'All' || n.dept === currentFilter;
        const matchSearch = n.subject.toLowerCase().includes(searchQuery.toLowerCase());
        return matchDept && matchSearch;
    });

    const totalPages = Math.ceil(filtered.length / rowsPerPage);
    

    if (currentPage > totalPages) currentPage = totalPages || 1;

    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const paginatedItems = filtered.slice(start, end);

    noticeCountSpan.textContent = `মোট: ${filtered.length}টি নোটিশ`;
    tableBody.innerHTML = '';

    if (paginatedItems.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5" class="text-center py-5 text-muted italic">কোনো নোটিশ পাওয়া যায়নি!</td></tr>';
        renderPaginationControls(0);
        return;
    }


    paginatedItems.forEach(n => {
        const badgeClass = n.dept === 'All' ? 'badge-all' : 'badge-dept';
        const row = `
            <tr>
                <td class="text-muted fw-bold">${n.sl}</td>
                <td><span class="notice-subject" onclick="showNotice(${n.id})">${n.subject}</span></td>
                <td><span class="dept-badge ${badgeClass}">${n.dept}</span></td>
                <td class="text-secondary small whitespace-nowrap">${n.date}</td>
                <td>
                    <div class="d-flex align-items-center justify-content-center gap-2">
                        <button class="btn-action btn-view" onclick="showNotice(${n.id})" title="নোটিশ দেখুন">
                            <i class="fa fa-eye"></i>
                        </button>
                        ${n.pdf_file ? `
                            <a href="${n.pdf_file}" target="_blank" onclick="event.stopPropagation()">
                                <button class="btn-action btn-download" title="ডাউনলোড করুন"><i class="fa fa-file-pdf"></i></button>
                            </a>
                        ` : `
                            <button class="btn-action btn-download" style="opacity: 0.3; cursor: not-allowed;" disabled><i class="fa fa-file-pdf"></i></button>
                        `}
                    </div>
                </td>
            </tr>`;
        tableBody.insertAdjacentHTML('beforeend', row);
    });

    
    renderPaginationControls(totalPages);
}


function renderPaginationControls(totalPages) {
    if (!paginationWrapper) return;
    paginationWrapper.innerHTML = '';

    if (totalPages <= 1) return; 

    const prevClass = currentPage === 1 ? 'disabled' : '';
    paginationWrapper.insertAdjacentHTML('beforeend', `
        <li class="page-item ${prevClass}">
            <a class="page-link" href="javascript:void(0)" onclick="changePage(${currentPage - 1})">পূর্ববর্তী</a>
        </li>
    `);

   
    for (let i = 1; i <= totalPages; i++) {
        const activeClass = currentPage === i ? 'active' : '';
        paginationWrapper.insertAdjacentHTML('beforeend', `
            <li class="page-item ${activeClass}">
                <a class="page-link" href="javascript:void(0)" onclick="changePage(${i})">${i}</a>
            </li>
        `);
    }


    const nextClass = currentPage === totalPages ? 'disabled' : '';
    paginationWrapper.insertAdjacentHTML('beforeend', `
        <li class="page-item ${nextClass}">
            <a class="page-link" href="javascript:void(0)" onclick="changePage(${currentPage + 1})">পরবর্তী</a>
        </li>
    `);
}


window.changePage = function(page) {
    currentPage = page;
    renderNotices();
    window.scrollTo({ top: 0, behavior: 'smooth' }); 
};



  searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value;
            renderNotices();
        });

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.getAttribute('data-filter');
        currentPage = 1;
        renderNotices();
    });
});

 const noticeModal = new bootstrap.Modal(document.getElementById('noticeModal'));
        window.showNotice = function(id) {
            const notice = NOTICES.find(n => n.id === id);
            if (!notice) return;

            document.getElementById('modal-dept').textContent = notice.dept;
            document.getElementById('modal-subject').textContent = notice.subject;
            document.getElementById('modal-date').textContent = notice.date;
            document.getElementById('modal-author').textContent = notice.author;
            document.getElementById('modal-description').textContent = notice.description;
            const pdfBtn = document.getElementById('pdf');
                if (notice.pdf_file) {
                    pdfBtn.href = notice.pdf_file;
                    pdfBtn.style.display = 'inline-flex';
                } else {
                    pdfBtn.href = "#";
                    pdfBtn.style.display = 'none';
                }

            noticeModal.show();
        };