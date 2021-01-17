const api = "http://localhost:5000"

/***********************************/
/* API call to dump and git commit */
/***********************************/

export const manualBackup = () =>
  fetch(`${api}/backup`, {method: 'GET'})


/***********************************/
/*       API calls for /admin      */
/***********************************/

export const resetAdmin = () =>
  fetch(`${api}/admin/reset`, {method: 'GET'})

export const getAdmin = () =>
  fetch(`${api}/admin`)
    .then(res => res.json())
    .then(data => data)

export const postAdminItem = (adminItem) =>
  fetch(`${api}/admin`, {method: 'POST',
                         headers: {
                           'Content-Type': 'application/json',
                         },
                         body: adminItem})

/*********************************/
/*      API calls for /items     */
/*********************************/

export const resetItems = () =>
  fetch(`${api}/items/reset`, {method: 'GET'})

export const getItems = () =>
  fetch(`${api}/items`, {method: 'GET'})
    .then(res => res.json())
    .then(data => data)

export const postItems = (item) =>
  fetch(`${api}/items`, {method: 'POST',
                         headers: {
                           'Content-Type': 'application/json',
                         },
                         body: item})


