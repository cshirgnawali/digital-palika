// ===============================================
// Digital Palika Analytics Dashboard
// analytics.js
// ===============================================

const analyticsData = window.analyticsData;

// ======================================================
// Budget Utilization Chart
// ======================================================

new Chart(document.getElementById("budgetChart"), {

    type: "doughnut",

    data: {

        labels: ["Spent", "Remaining"],

        datasets: [{

            data: [

                analyticsData.totalSpent,
                analyticsData.remainingBudget

            ],

            backgroundColor: [

                "#ffc107",
                "#198754"

            ],

            borderWidth: 2

        }]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                position: "bottom"

            }

        }

    }

});



// ======================================================
// Complaint Status Chart
// ======================================================

const complaintLabels =
    analyticsData.complaintStatus.map(item => item[0]);

const complaintValues =
    analyticsData.complaintStatus.map(item => item[1]);

new Chart(document.getElementById("complaintChart"), {

    type: "pie",

    data: {

        labels: complaintLabels,

        datasets: [{

            label: "Complaints",

            data: complaintValues,

            backgroundColor: [

                "#0d6efd",
                "#ffc107",
                "#198754",
                "#dc3545",
                "#6f42c1",
                "#20c997"

            ],

            borderWidth: 2

        }]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                position: "bottom"

            }

        }

    }

});



// ======================================================
// Project Status Chart
// ======================================================

const projectLabels =
    analyticsData.projectStatus.map(item => item[0]);

const projectValues =
    analyticsData.projectStatus.map(item => item[1]);

new Chart(document.getElementById("projectChart"), {

    type: "doughnut",

    data: {

        labels: projectLabels,

        datasets: [{

            label: "Projects",

            data: projectValues,

            backgroundColor: [

                "#6c757d",
                "#ffc107",
                "#198754",
                "#dc3545",
                "#0dcaf0",
                "#fd7e14"

            ],

            borderWidth: 2

        }]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                position: "bottom"

            }

        }

    }

});



// ======================================================
// Projects by Department
// ======================================================

const departmentLabels =
    analyticsData.projectsByDepartment.map(item => item[0]);

const departmentValues =
    analyticsData.projectsByDepartment.map(item => item[1]);

new Chart(document.getElementById("departmentChart"), {

    type: "bar",

    data: {

        labels: departmentLabels,

        datasets: [{

            label: "Projects",

            data: departmentValues,

            backgroundColor: [

                "#0d6efd",
                "#198754",
                "#ffc107",
                "#dc3545",
                "#6610f2",
                "#fd7e14",
                "#20c997",
                "#6f42c1"

            ],

            borderRadius: 8

        }]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                display: false

            }

        },

        scales: {

            y: {

                beginAtZero: true,

                ticks: {

                    precision: 0

                }

            }

        }

    }

});



// ======================================================
// Budget Allocation by Project
// ======================================================

const budgetProjectData = analyticsData.budgetByProject || [];

const budgetProjectLabels =
    budgetProjectData.map(item => item[0]);

const budgetProjectValues =
    budgetProjectData.map(item => item[1]);

new Chart(document.getElementById("budgetProjectChart"), {

    type: "bar",

    data: {

        labels: budgetProjectLabels,

        datasets: [{

            label: "Allocated Budget (Rs.)",

            data: budgetProjectValues,

            backgroundColor: "#20c997",

            borderRadius: 8

        }]

    },

    options: {

        responsive: true,

        indexAxis: "y",

        plugins: {

            legend: {

                display: false

            },

            title: {

                display: true,

                text: "Budget Allocation by Project"

            }

        },

        scales: {

            x: {

                beginAtZero: true,

                ticks: {

                    callback: function(value) {

                        return "Rs. " + Number(value).toLocaleString();

                    }

                }

            },

            y: {

                ticks: {

                    autoSkip: false

                }

            }

        }

    }

});
// ======================================================
// Projects by Ward
// ======================================================

const wardData = analyticsData.projectsByWard || [];

const wardLabels =
    wardData.map(item => "Ward " + item[0]);

const wardValues =
    wardData.map(item => item[1]);

new Chart(document.getElementById("wardChart"), {

    type: "bar",

    data: {

        labels: wardLabels,

        datasets: [{

            label: "Projects",

            data: wardValues,

            backgroundColor: [

                "#0d6efd",
                "#198754",
                "#ffc107",
                "#dc3545",
                "#6f42c1",
                "#fd7e14",
                "#20c997",
                "#0dcaf0",
                "#6610f2",
                "#adb5bd"

            ],

            borderRadius: 8

        }]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                display: false

            },

            title: {

                display: true,

                text: "Projects Distribution by Ward"

            }

        },

        scales: {

            y: {

                beginAtZero: true,

                ticks: {

                    precision: 0

                }

            }

        }

    }

});

// ======================================================
// Budget vs Spent by Department
// ======================================================

const budgetDepartmentData = analyticsData.budgetDepartment || [];

const departmentNames =
    budgetDepartmentData.map(item => item[0]);

const allocatedBudget =
    budgetDepartmentData.map(item => item[1]);

const spentBudget =
    budgetDepartmentData.map(item => item[2]);

new Chart(document.getElementById("budgetDepartmentChart"), {

    type: "bar",

    data: {

        labels: departmentNames,

        datasets: [

            {

                label: "Allocated Budget",

                data: allocatedBudget,

                backgroundColor: "#4e73df",

                borderRadius: 6

            },

            {

                label: "Spent Budget",

                data: spentBudget,

                backgroundColor: "#e74a3b",

                borderRadius: 6

            }

        ]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        plugins: {

    legend: {

        position: "top"

    },

    title: {

        display: true,

        text: "Department-wise Budget Comparison"

    },

    tooltip: {

        callbacks: {

            label: function(context) {

                return context.dataset.label +
                       ": Rs. " +
                       Number(context.raw).toLocaleString();

            }

        }

    }

},

        scales: {

    x: {

        ticks: {

            maxRotation: 30,
            minRotation: 30

        }

    },

    y: {

        beginAtZero: true,

        ticks: {

            callback: function(value) {

                return "Rs. " + Number(value).toLocaleString();

            }

        }

    }

}

    }

});