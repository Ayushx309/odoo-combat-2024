
// scripts.js
const companyList = document.getElementById('companyList');
const pagination = document.getElementById('pagination');
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');

let accountData = []; 
let currentPage = 1;
const itemsPerPage = 4;


function fetchAllAccounts() {
    fetch('/api/accounts', {
        headers: {
            'Authorization': '@**SPDS@**',
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            accountData = data.accounts; 
            console.log(accountData)
            handleSearch(); 
        })
        .catch(error => console.error('Error fetching accounts:', error));
}

// Function to handle search
function handleSearch() {
    const searchTerm = searchInput.value.trim().toLowerCase();

    // Filter data based on search term
    const filteredAccounts = accountData.filter(Account =>
        Account.username.toLowerCase().includes(searchTerm)
    );

    displayCompanies(filteredAccounts); // Call displayCompanies with filtered data
}

// Function to display companies for a given page
function displayCompanies(accounts) {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const displayedaccounts = accounts.slice(startIndex, endIndex);
    companyList.innerHTML = '';
    displayedaccounts.forEach(account => {
        const accountRow = document.createElement('tr');
        if (account.last_login === null) {
            account.last_login = "Not Logged in yet!";
        }
        accountRow.innerHTML = `
        <td class="table-img-name-key-main-container">
            <div class="table-img-name-key-container">
                <div class="table-img-container">
                    <img src="/static/assets/images/default.jpg"
                        alt="Company Logo" class="table-img" />
                </div>
                <div class="table-name-key-container">
                <span id="table-name">${account.username}</span>
                </div>
            </div>
                
            <div class="mobile-three-dots">
                <i data-id="${account.id}" class="fi fi-bs-menu-dots-vertical"></i>
            </div>


        </td>
        <td class="table-mobile-datacell" data-cell='display_name : '>${account.display_name}</td>
        <td class="table-mobile-datacell" data-cell='role : '>${account.role}</td>
        <td class="table-mobile-datacell" data-cell='last_login : '>${account.last_login}</td>
        <td class="table-mobile-datacell" data-cell='creation : '>${account.creation}</td>
        <td id="table-three-dots"><i ata-id="${account.id}" class="fi fi-bs-menu-dots-vertical"></i></td>
        `;

        companyList.appendChild(accountRow);
    });
    renderPagination(accounts.length);
}




// Function to render pagination
function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    pagination.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.textContent = i;
        pageButton.className = 'pagination_button';
        if (i === currentPage) {
            pageButton.classList.add('active');
        }
        pageButton.addEventListener('click', () => {
            currentPage = i;
            handleSearch();
        });
        pagination.appendChild(pageButton);
    }
}

// Event listeners
searchInput.addEventListener('input', handleSearch);
searchButton.addEventListener('click', handleSearch);

// Initial fetch of all accounts
fetchAllAccounts();

function openWindow(url, width, height) {
    // Calculate the left and top position to center the window
    const left = (window.innerWidth - width) / 2;
    const top = (window.innerHeight - height) / 2;

    // Open the new window with specified URL, size, and position
    window.open(url, '_blank', `width=${width}, height=${height}, left=${left}, top=${top}`);
}

// 
// 
// 
// context menu
// 
// 
// 

function fetchCompanyData(company_key, company_id) {
    const company = accountData.find(company => company.company_key === company_key) || null;

    if (company.company_bank_acc_type === "not_defined") {
        company.company_bank_acc_type = null;
    }

    const modalContent = document.getElementById("modal");
    modalContent.innerHTML = `
        <div class="close-div">
            <i class="fi fi-rs-circle-xmark close-button"></i>
        </div>
        <div class="dialog-main-container">
            <div class="dialog-company-primary-container">
                <div class="dialog-company-photo-name-key-container">
                    <div class="dialog-company-photo-container">
                        <img src="/static/${company.company_logo || "Assets/Images/default_company.jpg"}" class="dialog-company-photo"/>
                    </div>
                    <div class="dialog-company-name-key-container">
                        <span class="dialog-company-name">${company.company_name}</span>
                        <span class="dialog-company-key">${company.company_key}</span>
                    </div>
                </div>
                <div class="dialog-company-basics">
                    <div class="dialog-titlenattr">
                        <span>Phone No. : </span>
                        <span class="dialog-cbasic">${company.company_phone}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>Email : </span>
                        <span class="dialog-cbasic">${company.company_email}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>Address : </span>
                        <span class="dialog-cbasic">${company.company_address}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>Website : </span>
                        <span class="dialog-cbasic">${company.company_website}</span>
                    </div>
                </div>
            </div>
            <div class="dialog-company-secondary-container">
                <div class="dialog-company-tax-info">
                    <div class="dialog-titlenattr">
                        <span>GST No. : </span>
                        <span class="dialog-ctax">${company.company_gst_num || "Not Set"}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>UIN No. : </span>
                        <span class="dialog-ctax">${company.company_uin_num || "Not Set"}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>TDS No. : </span>
                        <span class="dialog-ctax">${company.company_tds_num || "Not Set"}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>PAN No. : </span>
                        <span class="dialog-ctax">${company.company_pan_num || "Not Set"}</span>
                    </div>
                </div>
                <div class="dialog-company-bank-info">
                    <div class="dialog-titlenattr">
                        <span>Bank Name : </span>
                        <span class="dialog-cbank">${company.company_bank_name || "Not Set"}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>Bank A/C No. : </span>
                        <span class="dialog-cbank">${company.company_bank_acc_num || "Not Set"}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>Bank A/C Type : </span>
                        <span class="dialog-cbank">${company.company_bank_acc_type || "Not Set"}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>Bank IFSC : </span>
                        <span class="dialog-cbank">${company.company_bank_ifsc_code || "Not Set"}</span>
                    </div>
                    <div class="dialog-titlenattr">
                        <span>Bank Branch : </span>
                        <span class="dialog-cbank">${company.company_bank_branch || "Not Set"}</span>
                    </div>
                </div>
                <div class="dialog-company-documents">
                    <div class="dialog-companydoc">
                        <span>Company Stamp : </span>
                        <div class="dialog-docimg">
                            <img src="/static/${company.company_stamp_photo || "Assets/Images/not_set.png"}" alt="Company Stamp">
                        </div>
                    </div>
                    <div class="dialog-companydoc">
                        <span>Company Signature : </span>
                        <div class="dialog-docimg">
                            <img src="/static/${company.company_signature_photo || "Assets/Images/not_set.png"}" alt="Company Signature">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="download-div">
            <button id="downloadButton"><i class="fi fi-rr-file-download"></i>Download Image</button>
        </div>
    `;

    const closeButton = document.querySelector(".close-button");
    closeButton.onclick = function () {
        modal.close();
        document.body.style.overflow = '';
    };

    const modal = document.getElementById("modal");
    modal.showModal();
    document.body.style.overflow = 'hidden';

    // Move this logic here to ensure elements are present
    const captureElement = document.querySelector('.dialog-company-primary-container');
    const downloadButton = document.getElementById('downloadButton');
    const keyHide = document.querySelector('.dialog-company-key');

    if (captureElement && downloadButton) {
        downloadButton.addEventListener('click', () => {
            keyHide.style.display = 'none';
            html2canvas(captureElement).then(canvas => {
                const image = canvas.toDataURL('image/png');
                const link = document.createElement('a');
                link.href = image;
                link.download = 'companyInfo.png';
                link.click();
                keyHide.style.display = '';
            }).catch(error => {
                console.error('Error capturing the element:', error);
                keyHide.style.display = '';
            });
        });
    } else {
        console.error('captureElement or downloadButton is not found in the DOM');
    }
}

$(function () {
    $.contextMenu({
        selector: '.fi-bs-menu-dots-vertical',
        trigger: 'left',
        callback: function (key, options) {
            var $icon = options.$trigger;
            var companyId = $icon.data('id');
            var companyKey = $icon.data('key');
            if (key === "view") {
                fetchCompanyData(companyKey, companyId);
            } else if (key === "edit") {
                window.location.assign(`/admin/masters/accounts/edit?id=${companyId}&key=${companyKey}`);
            } else if (key === "delete") {
                alert("Delete company with ID: " + companyId + " and Key: " + companyKey);
            }
        },
        items: {
            "view": { name: "View", icon: 'fas fa-eye' },
            "edit": { name: "Edit", icon: "edit" },
            "delete": { name: "Delete", icon: "delete", disabled: true },
            "sep1": "---------",
            "quit": { name: "Quit", icon: function ($element, key, item) { return 'context-menu-icon context-menu-icon-quit'; } }
        }
    });
});
