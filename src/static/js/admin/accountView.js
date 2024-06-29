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
        },method: 'post'
    })
        .then(response => response.json())
        .then(data => {
            accountData = data.accounts;
            console.log(accountData)
            handleSearch();
        })
        .catch(error => console.error('Error fetching accounts:', error));
}


function handleSearch() {
    const searchTerm = searchInput.value.trim().toLowerCase();
    const filteredAccounts = accountData.filter(Account =>
        Account.username.toLowerCase().includes(searchTerm)
    );

    displayCompanies(filteredAccounts);
}

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
                <i data-id="${account.id}" data-uname="${account.username}" class="fi fi-bs-menu-dots-vertical"></i>
            </div>


        </td>
        <td class="table-mobile-datacell" data-cell='display_name : '>${account.display_name}</td>
        <td class="table-mobile-datacell" data-cell='role : '>${account.role}</td>
        <td class="table-mobile-datacell" data-cell='last_login : '>${account.last_login}</td>
        <td class="table-mobile-datacell" data-cell='creation : '>${account.creation}</td>
        <td id="table-three-dots"><i data-id="${account.id}" data-uname="${account.username}" class="fi fi-bs-menu-dots-vertical"></i></td>
        `;

        companyList.appendChild(accountRow);
    });
    renderPagination(accounts.length);
}

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

searchInput.addEventListener('input', handleSearch);
searchButton.addEventListener('click', handleSearch);
fetchAllAccounts();

$(function () {
    $.contextMenu({
        selector: '.fi-bs-menu-dots-vertical',
        trigger: 'left',
        callback: function (key, options) {
            var $icon = options.$trigger;
            var accountId = $icon.data('id')
            var accountUname = $icon.data('uname')
            if (key === "edit") {
                window.location.assign(`/admin/accounts/edit?id=${accountId}`);
            } else if (key === "delete") {
                Swal.fire({
                    title: 'Delete Account',
                    text: "Are you sure you want to delete account with name: " + accountUname + "?",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes, delete it'
                }).then((result) => {
                    if (result.isConfirmed) {
                        $.ajax({
                            url: '/api/deleteAccount',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({ id: accountId }),
                            success: function (response) {
                                if (response.status === "success") {
                                    iziToast.success({
                                        title: 'Success',
                                        message: `Account successfully deleted.`,
                                        position: 'topRight',
                                    });
                                    fetchAllAccounts();
                                } else {
                                    Swal.fire(
                                        'Error!',
                                        response.message,
                                        'error'
                                    );
                                }
                            },
                            error: function (xhr, status, error) {
                                Swal.fire(
                                    'Error!',
                                    'An error occurred: ' + xhr.responseText,
                                    'error'
                                );
                            }
                        });
                    }
                });
            }
        },
        items: {
            "edit": { name: "Edit", icon: "edit" },
            "delete": { name: "Delete", icon: "delete" },
            "sep1": "---------",
            "quit": { name: "Quit", icon: function ($element, key, item) { return 'context-menu-icon context-menu-icon-quit'; } }
        }
    });
});
