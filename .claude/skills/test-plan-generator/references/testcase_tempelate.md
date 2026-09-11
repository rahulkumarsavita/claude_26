# Test Case: TC-001 - Create system Backup

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-001 |
| **Test Case Name** | Create system Backup |
| **Precondition** | User should logged in before |
| **Description** | N/A |
| **Expected Result** | User should be able to create stystem backup from web page |

---

## Test Steps

1. Cretae any Configuration client. On Clicking the Create Sys Backup Link a browse window should opened and user shoul be able to save the `ipaddress_backup (.zip)` file at any location locally on system.
2. After saving the backup file, unzip it and following items should be present there:
   * `configuration` folder
   * `Fonts` folder
   * `Images` Folder
   * `VideoTemplates` Folder
   * `cms.lic`
   * `cmsshare.properties`
   * `cmsversion.properties`
   * `healthdeamon.properties`