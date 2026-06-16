import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-accounts',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './accounts.html',
  styleUrl: './accounts.css'
})
export class Accounts implements OnInit {


  // ===============================
  // API URL
  // ===============================
  apiUrl = 'http://127.0.0.1:8000/api/accounts';


  // ===============================
  // Account Lists
  // ===============================

  accounts: any[] = [];
  filteredAccounts: any[] = [];


  // ===============================
  // Search
  // ===============================

  searchText = '';


  // ===============================
  // Summary Cards
  // ===============================

  totalAccounts = 0;
  connectedCount = 0;
  warningCount = 0;
  disconnectedCount = 0;


  // ===============================
  // Add/Edit Form
  // ===============================

  showAddForm = false;

  editMode = false;

  editingId = '';


  newAccount = {
    broker: 'Zerodha',
    client_id: '',
    name: '',
    role: 'Child',

    api_key: '',
    api_secret: '',
    access_token: ''
  };


  constructor(private http: HttpClient) {}


  // ===============================
  // Page Load
  // ===============================

  ngOnInit(): void {

    console.log("Accounts Module Started");

    this.loadAccounts();

  }



  // ===============================
  // GET Accounts
  // ===============================

  loadAccounts() {

    this.http
      .get<any>(this.apiUrl)
      .subscribe({

        next: (response) => {


          console.log(
            "Accounts API Response:",
            response
          );


          const data = response.accounts || [];


          this.accounts = data.map((acc:any)=>({

            id: acc.id,


            short:
              acc.broker
              ? acc.broker.charAt(0)
              : "A",


            broker: acc.broker,


            clientId:
              acc.client_id,


            name:
              acc.name,


            status:
              acc.status,


            statusClass:
              acc.status === "Connected"
              ? "connected"
              : acc.status === "Warning"
              ? "warning"
              : "disconnected",


            role:
              acc.role,


            roleClass:
              acc.role === "Master"
              ? "master"
              : "child",


            connection:
              acc.connection_info,


            session:
              acc.session_status,


            sync:
              acc.last_sync
              ? new Date(acc.last_sync)
                .toLocaleString()
              : "Never"

          }));


          // Copy for Search
          this.filteredAccounts =
            [...this.accounts];


          // Update Cards
          this.updateSummary();


          console.log(
            "Final Accounts:",
            this.accounts
          );


        },


        error:(error)=>{

          console.error(
            "Account Load Failed",
            error
          );

          alert(
            "Unable to load accounts"
          );

        }

      });

  }



  // ===============================
  // Summary Counter
  // ===============================

  updateSummary(){

    this.totalAccounts =
      this.accounts.length;


    this.connectedCount =
      this.accounts.filter(
        x=>x.status==="Connected"
      ).length;


    this.warningCount =
      this.accounts.filter(
        x=>x.status==="Warning"
      ).length;


    this.disconnectedCount =
      this.accounts.filter(
        x=>x.status==="Disconnected"
      ).length;


  }

    // ===============================
  // Open / Close Add Form
  // ===============================

  openAddAccount() {

    this.showAddForm = !this.showAddForm;

    if (!this.showAddForm) {
      this.resetForm();
    }

  }


  // ===============================
  // Save New Account (POST)
  // ===============================

  saveAccount() {

    this.http
      .post(this.apiUrl, this.newAccount)
      .subscribe({

        next: (response) => {

          console.log(
            "Account Created:",
            response
          );

          alert(
            "Account Added Successfully ✅"
          );

          this.resetForm();

          this.showAddForm = false;

          this.loadAccounts();

        },


        error: (error) => {

          console.error(
            "Create Account Error:",
            error
          );

          alert(
            "Failed to create account ❌"
          );

        }

      });

  }



  // ===============================
  // Edit Account
  // ===============================

  editAccount(account:any) {


    this.editMode = true;

    this.showAddForm = true;


    this.editingId = account.id;


    this.newAccount = {

      broker: account.broker,

      client_id: account.clientId,

      name: account.name,

      role: account.role,

      // Security reasons:
      // Backend usually does not return these
      api_key: "",

      api_secret: "",

      access_token: ""

    };


  }



  // ===============================
  // Update Account (PUT)
  // ===============================

  updateAccount() {


    this.http
      .put(
        `${this.apiUrl}/${this.editingId}`,
        this.newAccount
      )
      .subscribe({

        next: (response) => {


          console.log(
            "Account Updated:",
            response
          );


          alert(
            "Account Updated Successfully ✅"
          );


          this.resetForm();


          this.showAddForm = false;


          this.loadAccounts();


        },


        error: (error) => {


          console.error(
            "Update Failed:",
            error
          );


          alert(
            "Failed to update account ❌"
          );


        }


      });


  }



  // ===============================
  // Delete Account (DELETE)
  // ===============================

  deleteAccount(id:string) {


    const confirmDelete =
      confirm(
        "Are you sure you want to delete this account?"
      );


    if (!confirmDelete) {

      return;

    }


    this.http
      .delete(
        `${this.apiUrl}/${id}`
      )
      .subscribe({


        next: (response) => {


          console.log(
            "Account Deleted:",
            response
          );


          alert(
            "Account Deleted Successfully 🗑️"
          );


          this.loadAccounts();


        },


        error: (error) => {


          console.error(
            "Delete Error:",
            error
          );


          alert(
            "Unable to delete account ❌"
          );


        }


      });


  }



  // ===============================
  // Refresh Accounts
  // ===============================

  refreshAccounts() {

    this.loadAccounts();

  }



  // ===============================
  // Search Accounts
  // ===============================

  searchAccounts() {


    const value =
      this.searchText
        .toLowerCase()
        .trim();



    this.filteredAccounts =
      this.accounts.filter(acc =>


        acc.broker
          .toLowerCase()
          .includes(value)


        ||


        acc.clientId
          .toLowerCase()
          .includes(value)


        ||


        acc.name
          .toLowerCase()
          .includes(value)

      );


  }



  // ===============================
  // Reset Form
  // ===============================

  resetForm() {


    this.editMode = false;


    this.editingId = "";


    this.newAccount = {

      broker: "Zerodha",

      client_id: "",

      name: "",

      role: "Child",

      api_key: "",

      api_secret: "",

      access_token: ""

    };


  }

}