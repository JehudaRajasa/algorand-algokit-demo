const algosdk = require('algosdk');
require('dotenv').config();

// now we connect to the local server
const token = 'a'.repeat(64);
const server = 'http://localhost';
const port = 4002;
const client = new algosdk.Algodv2(token, server, port);

// Check your balance
async function getBalance(acct) {
  const acctInfo = await client.accountInformation(acct.addr).do();
  console.log(`Account balance: ${acctInfo.amount} microAlgos`);
}

// Get passphrase from environment variables
const pass = process.env.PASSPHRASE;
if (pass == undefined) {
  console.log('PASSPHRASE environment variable not set');
  process.exit(1);
}

// create account from passphrase
const acct = algosdk.mnemonicToSecretKey(pass);
getBalance(acct);

// build and send transactions
// here the input is the from account, the to address, the amount and note
async function sendPayment(acct, address2, amount, note) {
  const suggestedParams = await client.getTransactionParams().do();
  const ptxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
    from: acct.addr,
    suggestedParams,
    to: address2,
    amount: amount,
    note: new Uint8Array(Buffer.from(note))
  });

  // sign the transaction
  const signedTxn = ptxn.signTxn(acct.sk);

  // submit the transaction
  const { txId } = await client.sendRawTransaction(signedTxn).do();
  const result = await algosdk.waitForConfirmation(client, txId, 4);
  console.log(result);
  console.log(`Decoded Note: ${Buffer.from(result.txn.txn.note).toString()}`);
}

// We also need to add a check to get the ACCT2 address from the environment variable
// Get acct2 from environment variable
const acct2 = process.env.ACCT2;
if (acct2 == undefined) {
  console.log('ACCT2 environment variable not set');
  process.exit(1);
}

// Then later we call the function
// send payment
sendPayment(acct, acct2, 1000000, 'This is the first transaction');

// send asset to another account
async function sendAsset(acct, address2, assetIndex, amount) {
  // create transaction to send asset
  const suggestedParams = await client.getTransactionParams().do();
  const txn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
    from: acct.addr,
    suggestedParams,
    to: address2,
    assetIndex: assetIndex,
    amount: amount
  });

  const signedTxn = txn.signTxn(acct.sk);
  await client.sendRawTransaction(signedTxn).do();
  const result = await algosdk.waitForConfirmation(
    client,
    txn.txID().toString(),
    3
  );
  console.log(
    'asset transfer successful for amount ',
    result.txn.txn.aamt ? result.txn.txn.aamt : 0
  );
}

// later we need to call the function.
// You may notice we call it twice - the first time we use our own address and a 0 value to opt-in to the asset
// send asset - first we opt in to the asset
sendAsset(acct, acct.addr, 1010, 0);

// send asset to address2
sendAsset(acct, acct2, 1010, 1000);
