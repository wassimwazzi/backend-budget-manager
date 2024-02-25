BEGIN TRANSACTION;
--
-- Data for Name: category_category; Type: TABLE DATA; Schema: public; Owner: newwkfydyvglnv
--
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
(1, 'pbkdf2_sha256$720000$yC5X9aYUkoipbUeLYYEpRb$/0anGclFaaz33tDXKYDR93cxS0YjNO1rLzzjnyuQ5q0=', NULL, 0, 'wassimwazzi', '', '', '', 0, 1, '2023-12-25 17:24:31.402147+00'),
(2, 'pbkdf2_sha256$720000$KWRiBStnZZd9vy3qgQ7qJ6$vLtJMQZ6dqfMkjDwgZ1mKYMv15sIJ5xSipB9qn+O6/0=', NULL, 0, 'wassimsgirlfriend', 'Dara', 'Fakhoury', 'darafakhoury@gmail.com', 0, 1, '2023-12-25 22:33:36.72559+00'),
(4, 'pbkdf2_sha256$720000$dpyQTWBywSPAvZZBMgHKrs$/7pcVhLJyRQAC8OjvTk37aaQmTMJmdfRW9g5Jol8ZP4=', NULL, 0, 'testuser', 'test', '', '', 0, 1, '2023-12-26 19:46:44.901985+00'),
(5, 'pbkdf2_sha256$720000$NSXZXV0E9CfjVgeyeWwn7P$TUk5CMKbZddhDkUD+T4z76UM/wM7DNENxX9T+YwyOW4=', NULL, 0, 'demo', 'demo', 'user', '', 0, 1, '2023-12-28 17:48:39.153889+00'),
(6, 'pbkdf2_sha256$720000$wKzVIe87i9YcxnaBaVAAQ0$Yl5U6yxmG7zE481NF7WPRaF2ZTAtDhNuXPB0642wvo8=', NULL, 0, 'omar123', 'Omar', 'Kabalan', 'omarwkabalan@gmail.com', 0, 1, '2023-12-28 23:37:51.832983+00'),
(3, 'pbkdf2_sha256$720000$pSMX1HMI0KyUWFosETNv8o$u4tNXWoz2tDpN4hs1aNwBqYmwDALI2dVa+/EETgjVmw=', '2024-01-03 03:39:47.124185+00', 1, 'admin', '', '', '', 1, 1, '2023-12-25 23:31:47.477916+00')
;

INSERT INTO category_category VALUES (1, 'Salary', 1, 'Salary', 1, 0);
INSERT INTO category_category VALUES (2, 'Reimbursement', 1, 'E.g. Taxes', 1, 0);
INSERT INTO category_category VALUES (3, 'Other Income', 1, 'No specific category', 1, 1);
INSERT INTO category_category VALUES (5, 'Depanneur', 0, 'Convenience store', 1, 0);
INSERT INTO category_category VALUES (6, 'Education', 0, 'Education', 1, 0);
INSERT INTO category_category VALUES (7, 'Entertainment', 0, 'Entertainment', 1, 0);
INSERT INTO category_category VALUES (8, 'Fast Food', 0, 'Any food to go / fast food', 1, 0);
INSERT INTO category_category VALUES (9, 'Fees', 0, 'Any fees or unexpected payments', 1, 0);
INSERT INTO category_category VALUES (10, 'Food Delivery', 0, '', 1, 0);
INSERT INTO category_category VALUES (11, 'Gifts', 0, 'Gifts', 1, 0);
INSERT INTO category_category VALUES (12, 'Groceries', 0, 'Groceries', 1, 0);
INSERT INTO category_category VALUES (13, 'Health Care', 0, 'Health, beauty, massage, etc.', 1, 0);
INSERT INTO category_category VALUES (14, 'Home', 0, 'Items for home', 1, 0);
INSERT INTO category_category VALUES (15, 'Investments', 0, 'Investments', 1, 0);
INSERT INTO category_category VALUES (16, 'Other Expense', 0, 'No specific category', 1, 1);
INSERT INTO category_category VALUES (17, 'Restaurants', 0, '', 1, 0);
INSERT INTO category_category VALUES (18, 'Self Care', 0, 'Health, beauty, massage, etc.', 1, 0);
INSERT INTO category_category VALUES (19, 'Sports', 0, 'Sports', 1, 0);
INSERT INTO category_category VALUES (20, 'Subscriptions', 0, 'Subscriptions, e.g. Netflix', 1, 0);
INSERT INTO category_category VALUES (21, 'Transportation', 0, 'Transportation', 1, 0);
INSERT INTO category_category VALUES (22, 'Travel', 0, 'Travel', 1, 0);
INSERT INTO category_category VALUES (23, 'Utilities', 0, 'Utilities', 1, 0);
INSERT INTO category_category VALUES (4, 'Shopping', 0, 'Shopping', 1, 0);
INSERT INTO category_category VALUES (25, 'Reimbursement', 1, 'E.g. Taxes', 2, 0);
INSERT INTO category_category VALUES (26, 'Other Income', 1, 'No specific category', 2, 1);
INSERT INTO category_category VALUES (27, 'Shopping', 0, 'Shopping', 2, 0);
INSERT INTO category_category VALUES (28, 'Depanneur', 0, 'Convenience store', 2, 0);
INSERT INTO category_category VALUES (29, 'Education', 0, 'Education', 2, 0);
INSERT INTO category_category VALUES (30, 'Entertainment', 0, 'Entertainment', 2, 0);
INSERT INTO category_category VALUES (31, 'Fast Food', 0, 'Any food to go / fast food', 2, 0);
INSERT INTO category_category VALUES (32, 'Fees', 0, 'Any fees or unexpected payments', 2, 0);
INSERT INTO category_category VALUES (33, 'Food Delivery', 0, '', 2, 0);
INSERT INTO category_category VALUES (34, 'Gifts', 0, 'Gifts', 2, 0);
INSERT INTO category_category VALUES (35, 'Groceries', 0, 'Groceries', 2, 0);
INSERT INTO category_category VALUES (36, 'Health Care', 0, 'Health, beauty, massage, etc.', 2, 0);
INSERT INTO category_category VALUES (37, 'Home', 0, 'Items for home', 2, 0);
INSERT INTO category_category VALUES (38, 'Investments', 0, 'Investments', 2, 0);
INSERT INTO category_category VALUES (39, 'Other Expense', 0, 'No specific category', 2, 1);
INSERT INTO category_category VALUES (40, 'Restaurants', 0, '', 2, 0);
INSERT INTO category_category VALUES (41, 'Self Care', 0, 'Health, beauty, massage, etc.', 2, 0);
INSERT INTO category_category VALUES (42, 'Sports', 0, 'Sports', 2, 0);
INSERT INTO category_category VALUES (43, 'Subscriptions', 0, 'Subscriptions, e.g. Netflix', 2, 0);
INSERT INTO category_category VALUES (44, 'Transportation', 0, 'Transportation', 2, 0);
INSERT INTO category_category VALUES (45, 'Travel', 0, 'Travel', 2, 0);
INSERT INTO category_category VALUES (46, 'Utilities', 0, 'Utilities', 2, 0);
INSERT INTO category_category VALUES (24, 'Income', 1, 'Income', 2, 0);
INSERT INTO category_category VALUES (47, 'Uber', 0, 'Uber', 2, 0);
INSERT INTO category_category VALUES (48, 'Food', 0, 'Food Delivery/Unhealthy', 2, 0);
INSERT INTO category_category VALUES (49, 'Doctor', 0, 'Doctor', 2, 0);
INSERT INTO category_category VALUES (50, 'Grocery', 0, 'Grocery', 2, 0);
INSERT INTO category_category VALUES (51, 'Bills', 0, 'Bills', 2, 0);
INSERT INTO category_category VALUES (52, 'Rent', 0, 'Rent', 2, 0);
INSERT INTO category_category VALUES (53, 'Credit Card', 0, 'Credit Card Payment', 2, 0);
INSERT INTO category_category VALUES (54, 'Salary', 1, 'Salary', 3, 0);
INSERT INTO category_category VALUES (55, 'Reimbursement', 1, 'E.g. Taxes', 3, 0);
INSERT INTO category_category VALUES (56, 'Other Income', 1, 'No specific category', 3, 1);
INSERT INTO category_category VALUES (57, 'Shopping', 0, 'Shopping', 3, 0);
INSERT INTO category_category VALUES (58, 'Depanneur', 0, 'Convenience store', 3, 0);
INSERT INTO category_category VALUES (59, 'Education', 0, 'Education', 3, 0);
INSERT INTO category_category VALUES (60, 'Entertainment', 0, 'Entertainment', 3, 0);
INSERT INTO category_category VALUES (61, 'Fast Food', 0, 'Any food to go / fast food', 3, 0);
INSERT INTO category_category VALUES (62, 'Fees', 0, 'Any fees or unexpected payments', 3, 0);
INSERT INTO category_category VALUES (63, 'Food Delivery', 0, '', 3, 0);
INSERT INTO category_category VALUES (64, 'Gifts', 0, 'Gifts', 3, 0);
INSERT INTO category_category VALUES (65, 'Groceries', 0, 'Groceries', 3, 0);
INSERT INTO category_category VALUES (66, 'Health Care', 0, 'Health, beauty, massage, etc.', 3, 0);
INSERT INTO category_category VALUES (67, 'Home', 0, 'Items for home', 3, 0);
INSERT INTO category_category VALUES (68, 'Investments', 0, 'Investments', 3, 0);
INSERT INTO category_category VALUES (69, 'Other Expense', 0, 'No specific category', 3, 1);
INSERT INTO category_category VALUES (70, 'Restaurants', 0, '', 3, 0);
INSERT INTO category_category VALUES (71, 'Self Care', 0, 'Health, beauty, massage, etc.', 3, 0);
INSERT INTO category_category VALUES (72, 'Sports', 0, 'Sports', 3, 0);
INSERT INTO category_category VALUES (73, 'Subscriptions', 0, 'Subscriptions, e.g. Netflix', 3, 0);
INSERT INTO category_category VALUES (74, 'Transportation', 0, 'Transportation', 3, 0);
INSERT INTO category_category VALUES (75, 'Travel', 0, 'Travel', 3, 0);
INSERT INTO category_category VALUES (76, 'Utilities', 0, 'Utilities', 3, 0);
INSERT INTO category_category VALUES (77, 'Salary', 1, 'Salary', 4, 0);
INSERT INTO category_category VALUES (78, 'Reimbursement', 1, 'E.g. Taxes', 4, 0);
INSERT INTO category_category VALUES (79, 'Other Income', 1, 'No specific category', 4, 1);
INSERT INTO category_category VALUES (80, 'Shopping', 0, 'Shopping', 4, 0);
INSERT INTO category_category VALUES (81, 'Depanneur', 0, 'Convenience store', 4, 0);
INSERT INTO category_category VALUES (82, 'Education', 0, 'Education', 4, 0);
INSERT INTO category_category VALUES (83, 'Entertainment', 0, 'Entertainment', 4, 0);
INSERT INTO category_category VALUES (84, 'Fast Food', 0, 'Any food to go / fast food', 4, 0);
INSERT INTO category_category VALUES (85, 'Fees', 0, 'Any fees or unexpected payments', 4, 0);
INSERT INTO category_category VALUES (86, 'Food Delivery', 0, '', 4, 0);
INSERT INTO category_category VALUES (87, 'Gifts', 0, 'Gifts', 4, 0);
INSERT INTO category_category VALUES (88, 'Groceries', 0, 'Groceries', 4, 0);
INSERT INTO category_category VALUES (89, 'Health Care', 0, 'Health, beauty, massage, etc.', 4, 0);
INSERT INTO category_category VALUES (90, 'Home', 0, 'Items for home', 4, 0);
INSERT INTO category_category VALUES (91, 'Investments', 0, 'Investments', 4, 0);
INSERT INTO category_category VALUES (92, 'Other Expense', 0, 'No specific category', 4, 1);
INSERT INTO category_category VALUES (93, 'Restaurants', 0, '', 4, 0);
INSERT INTO category_category VALUES (94, 'Self Care', 0, 'Health, beauty, massage, etc.', 4, 0);
INSERT INTO category_category VALUES (95, 'Sports', 0, 'Sports', 4, 0);
INSERT INTO category_category VALUES (96, 'Subscriptions', 0, 'Subscriptions, e.g. Netflix', 4, 0);
INSERT INTO category_category VALUES (97, 'Transportation', 0, 'Transportation', 4, 0);
INSERT INTO category_category VALUES (98, 'Travel', 0, 'Travel', 4, 0);
INSERT INTO category_category VALUES (99, 'Utilities', 0, 'Utilities', 4, 0);
INSERT INTO category_category VALUES (100, 'Salary', 1, 'Salary', 5, 0);
INSERT INTO category_category VALUES (101, 'Reimbursement', 1, 'E.g. Taxes', 5, 0);
INSERT INTO category_category VALUES (102, 'Other Income', 1, 'No specific category', 5, 1);
INSERT INTO category_category VALUES (103, 'Shopping', 0, 'Shopping', 5, 0);
INSERT INTO category_category VALUES (104, 'Depanneur', 0, 'Convenience store', 5, 0);
INSERT INTO category_category VALUES (105, 'Education', 0, 'Education', 5, 0);
INSERT INTO category_category VALUES (106, 'Entertainment', 0, 'Entertainment', 5, 0);
INSERT INTO category_category VALUES (107, 'Fast Food', 0, 'Any food to go / fast food', 5, 0);
INSERT INTO category_category VALUES (108, 'Fees', 0, 'Any fees or unexpected payments', 5, 0);
INSERT INTO category_category VALUES (109, 'Food Delivery', 0, '', 5, 0);
INSERT INTO category_category VALUES (110, 'Gifts', 0, 'Gifts', 5, 0);
INSERT INTO category_category VALUES (111, 'Groceries', 0, 'Groceries', 5, 0);
INSERT INTO category_category VALUES (112, 'Health Care', 0, 'Health, beauty, massage, etc.', 5, 0);
INSERT INTO category_category VALUES (113, 'Home', 0, 'Items for home', 5, 0);
INSERT INTO category_category VALUES (114, 'Investments', 0, 'Investments', 5, 0);
INSERT INTO category_category VALUES (115, 'Other Expense', 0, 'No specific category', 5, 1);
INSERT INTO category_category VALUES (116, 'Restaurants', 0, '', 5, 0);
INSERT INTO category_category VALUES (117, 'Self Care', 0, 'Health, beauty, massage, etc.', 5, 0);
INSERT INTO category_category VALUES (118, 'Sports', 0, 'Sports', 5, 0);
INSERT INTO category_category VALUES (119, 'Subscriptions', 0, 'Subscriptions, e.g. Netflix', 5, 0);
INSERT INTO category_category VALUES (120, 'Transportation', 0, 'Transportation', 5, 0);
INSERT INTO category_category VALUES (121, 'Travel', 0, 'Travel', 5, 0);
INSERT INTO category_category VALUES (122, 'Utilities', 0, 'Utilities', 5, 0);
INSERT INTO category_category VALUES (123, 'Salary', 1, 'Salary', 6, 0);
INSERT INTO category_category VALUES (124, 'Reimbursement', 1, 'E.g. Taxes', 6, 0);
INSERT INTO category_category VALUES (125, 'Other Income', 1, 'No specific category', 6, 1);
INSERT INTO category_category VALUES (126, 'Shopping', 0, 'Shopping', 6, 0);
INSERT INTO category_category VALUES (127, 'Depanneur', 0, 'Convenience store', 6, 0);
INSERT INTO category_category VALUES (128, 'Education', 0, 'Education', 6, 0);
INSERT INTO category_category VALUES (129, 'Entertainment', 0, 'Entertainment', 6, 0);
INSERT INTO category_category VALUES (130, 'Fast Food', 0, 'Any food to go / fast food', 6, 0);
INSERT INTO category_category VALUES (131, 'Fees', 0, 'Any fees or unexpected payments', 6, 0);
INSERT INTO category_category VALUES (132, 'Food Delivery', 0, '', 6, 0);
INSERT INTO category_category VALUES (133, 'Gifts', 0, 'Gifts', 6, 0);
INSERT INTO category_category VALUES (134, 'Groceries', 0, 'Groceries', 6, 0);
INSERT INTO category_category VALUES (135, 'Health Care', 0, 'Health, beauty, massage, etc.', 6, 0);
INSERT INTO category_category VALUES (136, 'Home', 0, 'Items for home', 6, 0);
INSERT INTO category_category VALUES (137, 'Investments', 0, 'Investments', 6, 0);
INSERT INTO category_category VALUES (138, 'Other Expense', 0, 'No specific category', 6, 1);
INSERT INTO category_category VALUES (139, 'Restaurants', 0, '', 6, 0);
INSERT INTO category_category VALUES (140, 'Self Care', 0, 'Health, beauty, massage, etc.', 6, 0);
INSERT INTO category_category VALUES (141, 'Sports', 0, 'Sports', 6, 0);
INSERT INTO category_category VALUES (142, 'Subscriptions', 0, 'Subscriptions, e.g. Netflix', 6, 0);
INSERT INTO category_category VALUES (143, 'Transportation', 0, 'Transportation', 6, 0);
INSERT INTO category_category VALUES (144, 'Travel', 0, 'Travel', 6, 0);
INSERT INTO category_category VALUES (145, 'Utilities', 0, 'Utilities', 6, 0);


--
-- Data for Name: currency_currency; Type: TABLE DATA; Schema: public; Owner: newwkfydyvglnv
--

INSERT INTO currency_currency VALUES ('CAD');
INSERT INTO currency_currency VALUES ('LBP');
INSERT INTO currency_currency VALUES ('EUR');
INSERT INTO currency_currency VALUES ('USD');
INSERT INTO currency_currency VALUES ('GBP');


--
-- Data for Name: budget_budget; Type: TABLE DATA; Schema: public; Owner: newwkfydyvglnv
--

INSERT INTO budget_budget VALUES (1, 2050.00, '2023-10-01', 52, 'CAD', 2);
INSERT INTO budget_budget VALUES (2, 400.00, '2023-01-01', 50, 'CAD', 2);
INSERT INTO budget_budget VALUES (3, 400.00, '2023-01-01', 35, 'CAD', 2);
INSERT INTO budget_budget VALUES (4, 100.00, '2023-01-01', 8, 'CAD', 1);
INSERT INTO budget_budget VALUES (5, 40.00, '2023-01-01', 10, 'CAD', 1);
INSERT INTO budget_budget VALUES (6, 400.00, '2023-11-01', 17, 'CAD', 1);
INSERT INTO budget_budget VALUES (7, 300.00, '2023-01-01', 12, 'CAD', 1);
INSERT INTO budget_budget VALUES (8, 12.00, '2023-01-01', 20, 'CAD', 1);
INSERT INTO budget_budget VALUES (9, 40.00, '2023-01-01', 21, 'CAD', 1);
INSERT INTO budget_budget VALUES (10, 100.00, '2023-01-01', 19, 'CAD', 1);
INSERT INTO budget_budget VALUES (11, 50.00, '2023-01-01', 18, 'CAD', 1);
INSERT INTO budget_budget VALUES (12, 50.00, '2023-01-01', 4, 'CAD', 1);
INSERT INTO budget_budget VALUES (13, 1350.00, '2023-01-01', 14, 'CAD', 1);
INSERT INTO budget_budget VALUES (14, 300.00, '2023-01-01', 7, 'CAD', 1);
INSERT INTO budget_budget VALUES (16, 150.00, '2023-01-01', 17, 'CAD', 1);
INSERT INTO budget_budget VALUES (19, 150.00, '2023-12-01', 17, 'CAD', 1);
INSERT INTO budget_budget VALUES (20, 500.00, '2023-01-01', 106, 'CAD', 5);
INSERT INTO budget_budget VALUES (15, 150.00, '2023-01-01', 23, 'CAD', 1);

--
-- Data for Name: fileupload_fileupload; Type: TABLE DATA; Schema: public; Owner: newwkfydyvglnv
--
INSERT INTO fileupload_fileupload (id, file, date, status, message, user_id)
VALUES
(11, 'uploads/user-2/accountactivity_20231225223751.csv', '2023-12-25', 'FAILED', 'These income categories do not exist: Income
These expense categories do not exist: Clothes, Food, Grocery, Internet, Uber, Doctor
', 2),
(12, 'uploads/user-2/accountactivity_20231225224355.csv', '2023-12-25', 'COMPLETED', NULL, 2),
(13, 'uploads/user-4/dec18-21_20231226194708.csv', '2023-12-26', 'PENDING', NULL, 4),
(14, 'uploads/user-4/dec18-21_20231226195106.csv', '2023-12-26', 'PENDING', NULL, 4),
(15, 'uploads/user-4/dec18-21_20231226195530.csv', '2023-12-26', 'PENDING', NULL, 4),
(18, 'uploads/user-1/transactions_2023-12-25_20231226234225.csv', '2023-12-26', 'COMPLETED', NULL, 1),
(19, 'uploads/user-1/dec18-21_20231226234238.csv', '2023-12-26', 'COMPLETED', NULL, 1),
(21, 'uploads/user-1/accountactivity_20240119220751.csv', '2024-01-19', 'COMPLETED', NULL, 1),
(22, 'uploads/user-1/accountactivity_1_20240213133637.csv', '2024-02-13', 'FAILED', 'Missing columns: description
', 1),
(23, 'uploads/user-1/accountactivity_1_20240213133735.csv', '2024-02-13', 'COMPLETED', NULL, 1),
(24, 'uploads/user-1/accountactivity_2_20240221195914.csv', '2024-02-21', 'COMPLETED', NULL, 1),
(25, 'uploads/user-1/accountactivity_20240225234818.csv', '2024-02-25', 'FAILED', 'rows [1, 2, 3, 4, 5, 6, 7] have dates in the future
', 1),
(26, 'uploads/user-1/accountactivity_20240225235019.csv', '2024-02-25', 'FAILED', 'Error processing file', 1),
(27, 'uploads/user-1/accountactivity_20240225235224.csv', '2024-02-25', 'COMPLETED', NULL, 1)
;


--
-- Data for Name: transaction_transaction; Type: TABLE DATA; Schema: public; Owner: newwkfydyvglnv
--

INSERT INTO transaction_transaction (id, code, amount, date, description, inferred_category, category_id, currency_id, file_id, user_id)
VALUES
(1433, '', 2730.00, '2023-07-27', 'Salary', 0, 1, 'CAD', 18, 1),
(1434, '', 357.50, '2023-07-27', 'GST', 0, 2, 'CAD', 18, 1),
(1435, '', 52.00, '2023-07-27', 'Zara', 0, 2, 'CAD', 18, 1),
(1436, '', 6286.86, '2023-09-15', 'Morgan Stanley', 0, 1, 'CAD', 18, 1),
(719, 'FAMOUS PLAYER #   _M', 7.41, '2023-10-03', '', 1, 39, 'CAD', 12, 2),
(1437, '', 2005.45, '2023-09-29', 'Morgan Stanley', 0, 1, 'CAD', 18, 1),
(1438, '', 124.00, '2023-10-04', 'Canada GST', 0, 2, 'CAD', 18, 1),
(1439, '', 2005.45, '2023-10-13', 'Morgan stanley', 0, 1, 'CAD', 18, 1),
(723, 'FAMOUS PLAYER #   _M', 6.72, '2023-10-04', '', 1, 39, 'CAD', 12, 2),
(724, 'FAMOUS PLAYER #   _M', 12.29, '2023-10-05', '', 1, 39, 'CAD', 12, 2),
(1440, '', 1206.00, '2023-08-07', '900 USD I had from before', 0, 1, 'CAD', 18, 1),
(726, 'BLS INTERNATION   _M', 1.00, '2023-10-06', '', 1, 39, 'CAD', 12, 2),
(1441, '', 657.00, '2023-08-31', 'Convert leftover money from travel', 0, 2, 'CAD', 18, 1),
(1442, 'MORGAN STANLEY PAY', 2005.45, '2023-10-31', 'Salary Morgan Stanley', 0, 1, 'CAD', 18, 1),
(1443, 'CANADA           GST', 116.75, '2023-01-05', 'Tax reimbursement', 0, 2, 'CAD', 18, 1),
(1444, 'GOUV. QUEBEC     STC', 146.05, '2023-01-05', 'Tax reimbursement', 0, 2, 'CAD', 18, 1),
(732, 'PTS TO:  05276572907', 10.00, '2023-10-16', '', 1, 39, 'CAD', 12, 2),
(733, 'FAMOUS PLAYER #   _M', 6.03, '2023-10-16', '', 1, 39, 'CAD', 12, 2),
(1445, 'UHC OF QUEBEC', 185.00, '2023-01-23', '', 0, 2, 'CAD', 18, 1),
(1446, 'UHC OF QUEBEC', 104.37, '2023-01-23', 'Tax reimbursement', 0, 2, 'CAD', 18, 1),
(1447, 'B/M PAY-PAIE  PAY', 874.97, '2023-02-03', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1448, 'E-TRANSFER ***uJP', 60.00, '2023-02-06', 'Reimbursement', 0, 2, 'CAD', 18, 1),
(738, 'SQ *9493=4395 Q   _M', 15.00, '2023-10-17', '', 1, 39, 'CAD', 12, 2),
(1449, 'B/M PAY-PAIE  PAY', 874.99, '2023-02-17', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1450, 'E-TRANSFER ***Vzb', 200.00, '2023-02-21', 'Reimbursement', 0, 2, 'CAD', 18, 1),
(1451, 'GC 4575-DEPOSIT', 210.00, '2023-02-22', 'Reimbursement', 0, 2, 'CAD', 18, 1),
(1452, 'E-TRANSFER ***myQ', 184.00, '2023-03-01', 'Reimbursement', 0, 2, 'CAD', 18, 1),
(1453, 'B/M PAY-PAIE  PAY', 883.50, '2023-03-03', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1454, 'E-TRANSFER ***46D', 41.00, '2023-03-08', 'Reimbursement', 0, 2, 'CAD', 18, 1),
(1455, 'B/M PAY-PAIE  PAY', 1216.03, '2023-03-17', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1456, 'Radicle Group    EXP', 25.00, '2023-03-17', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1457, 'E-TRANSFER ***CJ9', 21.57, '2023-03-29', 'Reimbursement', 0, 2, 'CAD', 18, 1),
(1458, 'B/M PAY-PAIE  PAY', 1071.08, '2023-03-31', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1459, 'CANADA           GST', 116.75, '2023-04-05', 'Tax reimbursement', 0, 2, 'CAD', 18, 1),
(1460, 'GOUV. QUEBEC     STC', 146.05, '2023-04-05', 'Tax reimbursement', 0, 2, 'CAD', 18, 1),
(1461, 'B/M PAY-PAIE  PAY', 1267.17, '2023-04-14', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1462, 'CANADA           RIT', 919.02, '2023-04-27', 'Tax reimbursement', 0, 2, 'CAD', 18, 1),
(1463, 'GOUV. QUEBEC     TRP', 799.45, '2023-04-27', 'Tax reimbursement', 0, 2, 'CAD', 18, 1),
(1464, 'B/M PAY-PAIE  PAY', 977.29, '2023-04-28', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1465, 'E-TRANSFER ***297', 12.00, '2023-05-08', 'Reimbursement', 0, 2, 'CAD', 18, 1),
(1466, 'E-TRANSFER ***JBs', 15.00, '2023-05-08', 'Reimbursement', 0, 2, 'CAD', 18, 1),
(1467, 'B/M PAY-PAIE  PAY', 1637.46, '2023-05-12', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1468, 'B/M PAY-PAIE  PAY', 1550.62, '2023-05-26', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1469, 'B/M PAY-PAIE  PAY', 1675.58, '2023-06-09', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1470, 'B/M PAY-PAIE  PAY', 1550.62, '2023-06-23', 'Radicle Salary', 0, 1, 'CAD', 18, 1),
(1471, 'MORGAN STANLEY PAY', 2005.45, '2023-11-15', 'morgan stanley', 0, 1, 'CAD', 18, 1),
(1472, 'MORGAN STANLEY   PAY', 2005.45, '2023-11-30', '', 0, 1, 'CAD', 18, 1),
(1473, 'MORGAN STANLEY   PAY', 1976.09, '2023-12-15', '', 0, 1, 'CAD', 18, 1),
(1474, '', 1300.00, '2023-07-04', 'Rent', 0, 14, 'CAD', 18, 1),
(1475, '', 11.49, '2023-07-04', 'Spotify', 0, 20, 'CAD', 18, 1),
(1476, '', 4.59, '2023-07-04', 'COUCHETARD', 0, 5, 'CAD', 18, 1),
(1477, '', 50.42, '2023-07-04', 'ADONIS 21945 GR _F', 0, 12, 'CAD', 18, 1),
(1478, '', 64.56, '2023-07-04', 'France Visa', 0, 9, 'CAD', 18, 1),
(772, 'UBER* EATS PEND   _V', 24.11, '2023-10-30', '', 1, 39, 'CAD', 12, 2),
(1479, '', 35.09, '2023-07-04', 'MANULIFE TRAVEL _V', 0, 9, 'CAD', 18, 1),
(1480, '', 10.11, '2023-07-04', 'CULTURES PMT SA _F', 0, 8, 'CAD', 18, 1),
(1481, '', 19.61, '2023-07-04', 'AMIR _F', 0, 8, 'CAD', 18, 1),
(1482, '', 34.37, '2023-07-05', 'ZIBO GRIFFINTOW _F', 0, 17, 'CAD', 18, 1),
(1483, '', 8.75, '2023-07-06', 'PIZZA DANY _F', 0, 8, 'CAD', 18, 1),
(1484, '', 2.50, '2023-07-06', 'PIZZA DANY _F', 0, 8, 'CAD', 18, 1),
(1485, '', 4.17, '2023-07-06', 'COPIE NOVA _F', 0, 9, 'CAD', 18, 1),
(781, 'MONTHLY ACCOUNT FEE', 16.95, '2023-10-31', '', 1, 39, 'CAD', 12, 2),
(1486, '', 9.42, '2023-07-06', 'COMPTOIR DU CHE _F', 0, 8, 'CAD', 18, 1),
(1487, '', 23.52, '2023-07-06', 'METRO ETS 2416 _F', 0, 12, 'CAD', 18, 1),
(1488, '', 8.16, '2023-07-06', 'PROVIGO LE MARC _F', 0, 12, 'CAD', 18, 1),
(1489, '', 8.04, '2023-07-07', 'METRO ETS 2416 _F', 0, 12, 'CAD', 18, 1),
(1490, '', 21.00, '2023-07-07', 'STM LOGE PEEL O _F', 0, 21, 'CAD', 18, 1),
(787, 'UBER* PENDING     _V', 46.19, '2023-11-03', '', 1, 39, 'CAD', 12, 2),
(1491, '', 3.00, '2023-07-07', 'SQ *LE CAFE STR _F', 0, 8, 'CAD', 18, 1),
(789, 'UBR* PENDI   33.97_V', 48.19, '2023-11-07', '', 1, 39, 'CAD', 12, 2),
(1492, '', 50.59, '2023-07-10', 'SQ *09 SHERBROO', 0, 8, 'CAD', 18, 1),
(791, 'TD ATM W/D    009883', 60.00, '2023-11-08', '', 1, 39, 'CAD', 12, 2),
(792, 'UBER   TRI   34.22_V', 48.95, '2023-11-09', '', 1, 39, 'CAD', 12, 2),
(730, 'BCA RESEARCH IN  PAY', 1700.00, '2023-10-13', '', 1, 24, 'CAD', 12, 2),
(763, 'BCA RESEARCH IN  PAY', 1700.00, '2023-10-30', '', 1, 24, 'CAD', 12, 2),
(779, 'BCA RESEARCH IN  PAY', 1700.00, '2023-10-31', '', 1, 24, 'CAD', 12, 2),
(761, 'PHARMAPRIX #193   _M', 44.23, '2023-10-27', '', 1, 27, 'CAD', 12, 2),
(760, '550 - SEPHORA     _M', 152.22, '2023-10-27', '', 1, 27, 'CAD', 12, 2),
(716, 'GARAGE #222       _M', 57.37, '2023-10-03', '', 1, 27, 'CAD', 12, 2),
(714, 'SQ *ONGLERIE BE   _M', 15.60, '2023-10-03', '', 1, 27, 'CAD', 12, 2),
(790, 'UBER CANADA/UBE   _V', 35.46, '2023-11-08', '', 1, 47, 'CAD', 12, 2),
(782, 'UBER CANADA/UBE   _V', 44.83, '2023-11-01', '', 1, 47, 'CAD', 12, 2),
(778, '550 - SEPHORA     _M', 155.70, '2023-10-31', '', 1, 27, 'CAD', 12, 2),
(777, '550 - SEPHORA     _M', 100.00, '2023-10-31', '', 1, 27, 'CAD', 12, 2),
(774, 'UBER CANADA/UBE   _V', 23.00, '2023-10-31', '', 1, 47, 'CAD', 12, 2),
(773, 'UBER CANADA/UBE   _V', 25.86, '2023-10-30', '', 1, 47, 'CAD', 12, 2),
(771, 'UBER CANADA/UBE   _V', 38.50, '2023-10-30', '', 1, 47, 'CAD', 12, 2),
(788, 'SEND E-TFR ***mju', 2050.00, '2023-11-07', 'Rent', 0, 52, 'CAD', 12, 2),
(786, 'IW270 TFR-TO 6572907', 1000.00, '2023-11-02', 'Credit Card Payment', 0, 53, 'CAD', 12, 2),
(739, 'Spotify      12.64_V', 12.64, '2023-10-19', 'Subscriptions', 0, 43, 'CAD', 12, 2),
(748, 'SEND E-TFR ***muU', 600.00, '2023-10-23', 'Credit Card Payment', 0, 53, 'CAD', 12, 2),
(729, 'SEND E-TFR ***RFb', 2050.00, '2023-10-06', 'Rent', 0, 52, 'CAD', 12, 2),
(770, 'UBER CANADA/UBE   _V', 18.38, '2023-10-30', '', 1, 47, 'CAD', 12, 2),
(769, 'UBER CANADA/UBE   _V', 12.57, '2023-10-30', '', 1, 47, 'CAD', 12, 2),
(767, 'UBER CANADA/UBE   _V', 15.55, '2023-10-30', '', 1, 47, 'CAD', 12, 2),
(766, 'UBER CANADA/UBE   _V', 15.78, '2023-10-30', '', 1, 47, 'CAD', 12, 2),
(765, 'UBER CANADA/UBE   _V', 17.83, '2023-10-30', '', 1, 47, 'CAD', 12, 2),
(764, 'UBER CANADA/UBE   _V', 30.22, '2023-10-30', '', 1, 47, 'CAD', 12, 2),
(759, 'UBER CANADA/UBE   _V', 33.21, '2023-10-27', 'Transportation', 1, 47, 'CAD', 12, 2),
(749, 'UBER CANADA/UBE   _V', 32.99, '2023-10-23', '', 1, 47, 'CAD', 12, 2),
(745, 'UBER CANADA/UBE   _V', 44.39, '2023-10-20', '', 1, 47, 'CAD', 12, 2),
(743, 'UBER CANADA/UBE   _V', 10.62, '2023-10-20', '', 1, 47, 'CAD', 12, 2),
(742, 'UBER CANADA/UBE   _V', 25.86, '2023-10-20', '', 1, 47, 'CAD', 12, 2),
(794, 'OLLY FRESCO''S C   _M', 1.14, '2023-11-09', '', 1, 48, 'CAD', 12, 2),
(793, 'OLLY FRESCO''S C   _M', 1.71, '2023-11-09', '', 1, 48, 'CAD', 12, 2),
(785, 'LA FABRIQUE DE    _M', 4.63, '2023-11-02', '', 1, 48, 'CAD', 12, 2),
(784, 'OLLY FRESCO''S C   _M', 12.51, '2023-11-02', '', 1, 48, 'CAD', 12, 2),
(1493, '', 62.37, '2023-07-10', 'JAM INDUSTRIES _V', 0, 4, 'CAD', 18, 1),
(783, 'LEAVES HOUSE MC   _M', 9.08, '2023-11-02', '', 1, 48, 'CAD', 12, 2),
(780, 'ESCONDITE         _M', 39.46, '2023-10-31', '', 1, 48, 'CAD', 12, 2),
(776, 'OLLY FRESCO''S C   _M', 1.71, '2023-10-31', '', 1, 48, 'CAD', 12, 2),
(775, 'TOM-Le Blossom    _M', 23.80, '2023-10-31', '', 1, 48, 'CAD', 12, 2),
(768, 'O FOUR            _M', 62.41, '2023-10-30', '', 1, 48, 'CAD', 12, 2),
(762, 'WIENSTEIN & GAV   _F', 41.40, '2023-10-27', '', 1, 48, 'CAD', 12, 2),
(758, 'LA FABRIQUE DE    _M', 4.63, '2023-10-26', '', 1, 48, 'CAD', 12, 2),
(757, 'KARMA POKE        _M', 25.78, '2023-10-26', '', 1, 48, 'CAD', 12, 2),
(756, 'LEAVES HOUSE MC   _M', 9.49, '2023-10-26', '', 1, 48, 'CAD', 12, 2),
(755, 'LA FABRIQUE DE    _M', 4.63, '2023-10-25', '', 1, 48, 'CAD', 12, 2),
(754, 'OLLY FRESCO''S C   _M', 1.71, '2023-10-25', '', 1, 48, 'CAD', 12, 2),
(752, 'LA FABRIQUE DE    _M', 4.54, '2023-10-24', '', 1, 48, 'CAD', 12, 2),
(751, 'OLLY FRESCO''S C   _M', 1.71, '2023-10-24', '', 1, 48, 'CAD', 12, 2),
(747, 'SHAWARMAZ PEEL    _M', 5.74, '2023-10-23', '', 1, 48, 'CAD', 12, 2),
(741, 'OLLY FRESCO''S C   _M', 5.73, '2023-10-19', '', 1, 48, 'CAD', 12, 2),
(740, 'OLLY FRESCO''S C   _M', 17.43, '2023-10-19', '', 1, 48, 'CAD', 12, 2),
(737, 'OLLY FRESCO''S C   _M', 1.71, '2023-10-17', '', 1, 48, 'CAD', 12, 2),
(736, 'Patisserie Mahr   _M', 26.10, '2023-10-16', '', 1, 48, 'CAD', 12, 2),
(731, 'AMEA CAFE         _M', 51.55, '2023-10-16', '', 1, 48, 'CAD', 12, 2),
(728, 'STARBUCKS 800-7   _V', 13.11, '2023-10-06', '', 1, 48, 'CAD', 12, 2),
(725, 'OLLY FRESCO''S C   _M', 10.53, '2023-10-05', '', 1, 48, 'CAD', 12, 2),
(721, 'OLLY FRESCO''S C   _M', 21.77, '2023-10-03', '', 1, 48, 'CAD', 12, 2),
(720, 'OLLY FRESCO''S C   _M', 5.12, '2023-10-03', '', 1, 48, 'CAD', 12, 2),
(718, 'STARBUCKS COFFE   _M', 13.62, '2023-10-03', '', 1, 48, 'CAD', 12, 2),
(717, 'STARBUCKS COFFE   _M', 8.41, '2023-10-03', '', 1, 48, 'CAD', 12, 2),
(715, 'CAFFETTIERA CAF   _M', 17.19, '2023-10-03', '', 1, 48, 'CAD', 12, 2),
(753, 'CREAMED CLINIQU   _M', 243.99, '2023-10-24', '', 1, 49, 'CAD', 12, 2),
(750, 'PROVIGO LE MARC   _M', 91.31, '2023-10-23', '', 1, 50, 'CAD', 12, 2),
(746, 'PROVIGO LE MARC   _M', 70.86, '2023-10-23', '', 1, 50, 'CAD', 12, 2),
(744, 'PROVIGO LE MARC   _M', 14.37, '2023-10-20', '', 1, 50, 'CAD', 12, 2),
(735, 'PROVIGO LE MARC   _M', 25.20, '2023-10-16', '', 1, 50, 'CAD', 12, 2),
(734, 'PROVIGO LE MARC   _M', 22.06, '2023-10-16', '', 1, 50, 'CAD', 12, 2),
(722, 'PROVIGO LE MARC   _M', 68.00, '2023-10-03', '', 1, 50, 'CAD', 12, 2),
(727, 'VIDEOTRON LTEE    _V', 284.02, '2023-10-06', '', 1, 51, 'CAD', 12, 2),
(795, 'UBER CANADA/UBE   _V', 25.84, '2023-11-09', 'Transportation', 0, 47, 'CAD', 12, 2),
(1494, '', 31.46, '2023-07-10', 'PROVIGO LE MARC _F', 0, 12, 'CAD', 18, 1),
(1495, '', 18.52, '2023-07-10', 'SOCIETE DU PARC _F', 0, 17, 'CAD', 18, 1),
(1496, '', 10.46, '2023-07-10', 'UBER CANADA/UBE _V', 0, 21, 'CAD', 18, 1),
(1497, '', 60.82, '2023-07-10', 'O FOUR _F', 0, 17, 'CAD', 18, 1),
(1498, '', 4.59, '2023-07-10', 'COUCHETARD #749 _F', 0, 5, 'CAD', 18, 1),
(1499, '', 3.95, '2023-07-10', 'COUCHETARD #568 _F', 0, 5, 'CAD', 18, 1),
(1500, '', 23.52, '2023-07-10', 'FIDO MOBILE BPY', 0, 23, 'CAD', 18, 1),
(1501, '', 48.27, '2023-07-11', 'METRO ETS 2416 _F', 0, 12, 'CAD', 18, 1),
(1502, '', 57.49, '2023-07-11', 'VIRGIN PLUS BPY', 0, 23, 'CAD', 18, 1),
(1503, '', 28.73, '2023-07-14', 'JEAN COUTU 385 _F', 0, 9, 'CAD', 18, 1),
(1504, '', 30.00, '2023-07-14', 'SEND E-TFR ***FsH', 0, 7, 'CAD', 18, 1),
(1505, '', 15.00, '2023-07-14', 'SEND E-TFR *j6e', 0, 7, 'CAD', 18, 1),
(1506, '', 10.00, '2023-07-14', 'PROVIGO LE MARC _F', 0, 12, 'CAD', 18, 1),
(1507, '', 2.90, '2023-07-17', 'COPIE CONCORDIA _F', 0, 9, 'CAD', 18, 1),
(1508, '', 200.00, '2023-07-17', 'APPLE.COM/CA _V', 0, 4, 'CAD', 18, 1),
(1509, '', 4.40, '2023-07-17', 'PIZZA DANY _F', 0, 8, 'CAD', 18, 1),
(1510, '', 6.44, '2023-07-17', 'MARCHE STANLEY _F', 0, 5, 'CAD', 18, 1),
(1511, '', 1556.76, '2023-07-17', 'APPLE.COM/CA _V', 0, 4, 'CAD', 18, 1),
(1512, '', 23.97, '2023-07-17', 'UBER EATS PEND _V', 0, 10, 'CAD', 18, 1),
(1513, '', 12.65, '2023-07-17', 'METRO ETS 2416 _F', 0, 12, 'CAD', 18, 1),
(1514, '', 19.96, '2023-07-17', 'MCDONALD''S #405', 0, 8, 'CAD', 18, 1),
(1515, '', 7.25, '2023-07-17', 'PAYBYPHONE CITY _V', 0, 21, 'CAD', 18, 1),
(1516, '', 11.49, '2023-07-18', 'UBER CANADA/UBE _V', 0, 10, 'CAD', 18, 1),
(1517, '', 19.98, '2023-07-19', 'UBER CANADA/UBE _V', 0, 10, 'CAD', 18, 1),
(1518, '', 1.18, '2023-07-19', 'EXPERT SHIPPING _F', 0, 9, 'CAD', 18, 1),
(1519, '', 1.15, '2023-07-19', 'EXPERT SHIPPING _F', 0, 9, 'CAD', 18, 1),
(1520, '', 23.08, '2023-07-21', 'UBER EATS PEND _V', 0, 10, 'CAD', 18, 1),
(1521, '', 36.37, '2023-07-24', 'ADONIS 21945 GR _F', 0, 12, 'CAD', 18, 1),
(1522, '', 10.21, '2023-07-24', 'MCDONALD''S #400 _F', 0, 8, 'CAD', 18, 1),
(1523, '', 35.00, '2023-07-24', 'CINEPLEX ENTERT _V', 0, 7, 'CAD', 18, 1),
(1524, '', 16.36, '2023-07-24', 'COUCHETARD #568 _F', 0, 5, 'CAD', 18, 1),
(1525, '', 27.78, '2023-07-24', 'METRO ETS 2416 _F', 0, 12, 'CAD', 18, 1),
(1526, '', 7.00, '2023-07-24', 'STM LUCIEN L AL', 0, 21, 'CAD', 18, 1),
(1527, '', 100.00, '2023-07-24', 'SEND E-TFR ***NU3', 0, 7, 'CAD', 18, 1),
(1528, '', 23.60, '2023-07-25', 'UBER CANADA/UBE _V', 0, 8, 'CAD', 18, 1),
(1529, '', 58.74, '2023-07-26', 'INDIGO 282 _F', 0, 6, 'CAD', 18, 1),
(1530, '', 287.25, '2023-07-26', 'VF SERVICES (CA', 0, 9, 'CAD', 18, 1),
(1531, '', 21.42, '2023-07-26', 'METRO ETS 2416 _F', 0, 12, 'CAD', 18, 1),
(1532, '', 42.50, '2023-07-27', 'Barber', 0, 18, 'CAD', 18, 1),
(1533, '', 25.00, '2023-07-27', 'Cleo', 0, 7, 'CAD', 18, 1),
(1534, '', 1300.00, '2023-09-01', 'Rent', 0, 14, 'CAD', 18, 1),
(1535, '', 5.74, '2023-09-01', 'IGA', 0, 12, 'CAD', 18, 1),
(1536, '', 3.67, '2023-09-01', 'McDonald’s', 0, 8, 'CAD', 18, 1),
(1537, '', 4.09, '2023-09-02', 'Metro', 0, 12, 'CAD', 18, 1),
(1538, '', 19.87, '2023-09-02', 'Metro', 0, 12, 'CAD', 18, 1),
(1539, '', 115.00, '2023-09-02', 'Flyjin', 0, 7, 'CAD', 18, 1),
(1540, '', 11.49, '2023-09-03', 'Spotify', 0, 20, 'CAD', 18, 1),
(1541, '', 24.11, '2023-09-05', 'uber eats', 0, 10, 'CAD', 18, 1),
(1542, '', 25.33, '2023-09-05', 'STORE # 1258      _V (idk?)', 0, 16, 'CAD', 18, 1),
(1543, '', 1.44, '2023-09-06', 'BIXI MONTREAL     _V', 0, 21, 'CAD', 18, 1),
(1544, '', 3.00, '2023-09-06', 'USAT_TD710227     _F', 0, 9, 'CAD', 18, 1),
(1545, '', 0.69, '2023-09-07', 'BIXI MONTREAL     _V', 0, 21, 'CAD', 18, 1),
(1546, '', 47.96, '2023-09-07', 'Phone', 0, 23, 'CAD', 18, 1),
(1547, '', 3.49, '2023-09-08', 'Juice for pre', 0, 5, 'CAD', 18, 1),
(1548, '', 3.74, '2023-09-08', 'Uber split', 0, 21, 'CAD', 18, 1),
(1549, '', 6.53, '2023-09-08', 'McDonald’s', 0, 8, 'CAD', 18, 1),
(1550, '', 48.00, '2023-09-08', 'E-transfer to geday for sahra', 0, 7, 'CAD', 18, 1),
(1551, '', 118.66, '2023-09-09', 'Enfants terribles Muna and Loulou', 0, 17, 'CAD', 18, 1),
(1552, '', 4.64, '2023-09-11', 'Uber eats', 0, 10, 'CAD', 18, 1),
(1553, '', 25.00, '2023-09-11', 'Amazon (remote + batteries)', 0, 4, 'CAD', 18, 1),
(1554, '', 25.47, '2023-09-11', 'Metro', 0, 12, 'CAD', 18, 1),
(1555, '', 57.50, '2023-09-11', 'Wifi', 0, 23, 'CAD', 18, 1),
(1556, '', 35.00, '2023-09-13', 'Barber', 0, 18, 'CAD', 18, 1),
(1557, '', 114.00, '2023-09-14', 'Catchart Morgan Stanley', 0, 7, 'CAD', 18, 1),
(1558, '', 50.00, '2023-09-15', 'Flyjin Morgan Stanley', 0, 7, 'CAD', 18, 1),
(1559, '', 25.00, '2023-09-16', 'Dentist', 0, 18, 'CAD', 18, 1),
(1560, '', 40.00, '2023-09-16', 'Hello Fresh', 0, 12, 'CAD', 18, 1),
(1561, '', 12.00, '2023-09-17', 'Amazon (floss)', 0, 12, 'CAD', 18, 1),
(1562, '', 54.00, '2023-09-14', 'Metro', 0, 12, 'CAD', 18, 1),
(1563, '', 9.73, '2023-09-18', 'MCDONALD''S', 0, 8, 'CAD', 18, 1),
(1564, '', 20.00, '2023-09-19', 'Morgan Stanley casino night', 0, 7, 'CAD', 18, 1),
(1565, '', 14.27, '2023-09-19', 'METRO', 0, 12, 'CAD', 18, 1),
(1566, '', 20.00, '2023-09-20', 'Morgan Stanley cafeteria', 0, 8, 'CAD', 18, 1),
(1567, '', 12.30, '2023-09-20', 'provigo', 0, 12, 'CAD', 18, 1),
(1568, '', 17.00, '2023-09-21', 'Monopole wine bar', 0, 7, 'CAD', 18, 1),
(1569, '', 10.20, '2023-09-21', 'McDonald’s', 0, 8, 'CAD', 18, 1),
(1570, '', 37.20, '2023-09-22', 'cineplex', 0, 7, 'CAD', 18, 1),
(1571, '', 93.00, '2023-09-22', 'Shodan', 0, 17, 'CAD', 18, 1),
(1572, '', 31.30, '2023-09-23', 'BBQ', 0, 12, 'CAD', 18, 1),
(1573, '', 78.20, '2023-09-23', 'HelloFresh', 0, 12, 'CAD', 18, 1),
(1574, '', 30.00, '2023-09-23', 'Intramurals jersey', 0, 4, 'CAD', 18, 1),
(1575, '', 31.00, '2023-09-24', 'Metro', 0, 12, 'CAD', 18, 1),
(1576, '', 20.00, '2023-09-25', 'Metro', 0, 12, 'CAD', 18, 1),
(1577, '', 80.30, '2023-09-26', 'Hydro Quebec', 0, 23, 'CAD', 18, 1),
(1578, '', 4.20, '2023-09-27', 'Floss', 0, 18, 'CAD', 18, 1),
(1579, '', 35.40, '2023-09-27', 'uber eats', 0, 10, 'CAD', 18, 1),
(1580, '', 13.80, '2023-09-28', 'Morgan Stanley cafeteria', 0, 8, 'CAD', 18, 1),
(1581, '', 7.00, '2023-09-28', 'Metro tickets', 0, 21, 'CAD', 18, 1),
(1582, '', 25.40, '2023-09-28', 'Fitzroy bar', 0, 7, 'CAD', 18, 1),
(1583, '', 10.20, '2023-09-28', 'McDonald’s', 0, 8, 'CAD', 18, 1),
(1584, '', 17.00, '2023-09-29', 'Account fee', 0, 9, 'CAD', 18, 1),
(1585, '', 1.30, '2023-09-30', 'Dep', 0, 5, 'CAD', 18, 1),
(1586, '', 37.00, '2023-09-30', 'Provigo', 0, 12, 'CAD', 18, 1),
(1587, '', 7.00, '2023-09-30', 'stm metro', 0, 21, 'CAD', 18, 1),
(1588, '', 29.00, '2023-09-30', 'piknic drinks', 0, 7, 'CAD', 18, 1),
(1589, '', 15.00, '2023-09-30', 'Picnic food', 0, 8, 'CAD', 18, 1),
(1590, '', 21.00, '2023-09-30', 'McDonald’s', 0, 8, 'CAD', 18, 1),
(1591, '', 17.00, '2023-09-30', 'Banking fee', 0, 9, 'CAD', 18, 1),
(1592, '', 1300.00, '2023-10-01', 'Rent', 0, 14, 'CAD', 18, 1),
(1593, '', 12.64, '2023-10-03', 'Spotify 12.64_V', 0, 20, 'CAD', 18, 1),
(1594, '', 28.00, '2023-10-03', 'Uber eats', 0, 10, 'CAD', 18, 1),
(1595, '', 71.50, '2023-10-04', 'Kinton Ramen', 0, 17, 'CAD', 18, 1),
(1596, '', 21.80, '2023-10-05', 'Amir', 0, 8, 'CAD', 18, 1),
(1597, '', 12.70, '2023-10-06', 'metro', 0, 12, 'CAD', 18, 1),
(1598, '', 42.50, '2023-10-06', 'haircut', 0, 18, 'CAD', 18, 1),
(1599, '', 16.10, '2023-10-07', 'Über eats', 0, 10, 'CAD', 18, 1),
(1600, '', 22.00, '2023-10-07', 'saq', 0, 7, 'CAD', 18, 1),
(1601, '', 5.50, '2023-10-07', 'Über', 0, 21, 'CAD', 18, 1),
(1602, '', 13.30, '2023-10-07', 'Couchetard cigs', 0, 5, 'CAD', 18, 1),
(1603, '', 5.00, '2023-10-07', 'Flyjin bathroom tip', 0, 9, 'CAD', 18, 1),
(1604, '', 50.00, '2023-10-07', 'Flyjin', 0, 7, 'CAD', 18, 1),
(1605, '', 11.10, '2023-10-07', 'Über', 0, 21, 'CAD', 18, 1),
(1606, '', 28.00, '2023-10-08', 'Uber eats', 0, 10, 'CAD', 18, 1),
(1607, '', 9.29, '2023-10-10', 'Über', 0, 21, 'CAD', 18, 1),
(1608, '', 46.50, '2023-10-10', 'Virgin phone', 0, 23, 'CAD', 18, 1),
(1609, '', 19.52, '2023-10-11', 'provigo', 0, 12, 'CAD', 18, 1),
(1610, '', 57.50, '2023-10-11', 'Virgin wifi', 0, 23, 'CAD', 18, 1),
(1611, '', 15.66, '2023-10-12', 'metro', 0, 12, 'CAD', 18, 1),
(1612, '', 36.62, '2023-10-12', 'Uber eats', 0, 10, 'CAD', 18, 1),
(1613, '', 49.60, '2023-10-14', 'deville', 0, 17, 'CAD', 18, 1),
(1614, '', 2657.00, '2023-10-15', 'Send 2000 usd to nido', 0, 11, 'CAD', 18, 1),
(1615, '', 5.30, '2023-10-15', 'Couchetard mcmuffin', 0, 8, 'CAD', 18, 1),
(1616, '', 26.50, '2023-10-15', 'Amen cafe', 0, 17, 'CAD', 18, 1),
(1617, '', 13.00, '2023-10-17', 'Dispensa', 0, 8, 'CAD', 18, 1),
(1618, '', 28.60, '2023-10-17', 'monopole', 0, 7, 'CAD', 18, 1),
(1619, '', 12.00, '2023-10-17', 'Altar grill', 0, 8, 'CAD', 18, 1),
(1620, '', 20.00, '2023-10-18', 'provigo', 0, 12, 'CAD', 18, 1),
(1621, '', 7.35, '2023-10-20', 'McDonald’s', 0, 8, 'CAD', 18, 1),
(1622, '', 17.40, '2023-10-20', 'Uber eats', 0, 10, 'CAD', 18, 1),
(1623, '', 14.00, '2023-10-21', 'Uber eats', 0, 10, 'CAD', 18, 1),
(1624, '', 70.55, '2023-10-21', 'Cloakroom bar', 0, 7, 'CAD', 18, 1),
(1625, '', 23.00, '2023-10-23', 'Pizzeria 900', 0, 17, 'CAD', 18, 1),
(1626, '', 32.12, '2023-10-23', 'Uber eats groceries', 0, 12, 'CAD', 18, 1),
(1627, '', 17.40, '2023-10-24', 'Adonis food', 0, 8, 'CAD', 18, 1),
(1628, '', 6.50, '2023-10-25', 'pharmacie', 0, 18, 'CAD', 18, 1),
(1629, '', 19.20, '2023-10-25', 'Provigo food', 0, 8, 'CAD', 18, 1),
(1630, '', 7.82, '2023-10-26', 'MS cafeteria', 0, 8, 'CAD', 18, 1),
(1631, '', 55.30, '2023-10-26', 'moretti', 0, 17, 'CAD', 18, 1),
(1632, '', 22.00, '2023-10-27', 'metro', 0, 12, 'CAD', 18, 1),
(1633, '', 800.00, '2023-10-27', 'Nido ticket', 0, 11, 'CAD', 18, 1),
(1634, '', 16.66, '2023-10-27', 'Pharmaprix shampoo', 0, 12, 'CAD', 18, 1),
(1635, 'EPICERIE FINE I _F', 8.00, '2023-10-27', 'italimenti', 0, 8, 'CAD', 18, 1),
(1636, '', 1300.00, '2023-08-01', 'Rent', 0, 14, 'CAD', 18, 1),
(1637, '', 3000.00, '2023-07-31', 'McGill Loan', 0, 9, 'CAD', 18, 1),
(1638, '', 48.00, '2023-08-01', 'Virgin Phone', 0, 23, 'CAD', 18, 1),
(1639, '', 40.00, '2023-08-01', 'Bailey’s SAQ', 0, 7, 'CAD', 18, 1),
(1640, '', 34.00, '2023-08-01', 'Parking Fine Ottawa', 0, 9, 'CAD', 18, 1),
(1641, '', 30.00, '2023-08-02', 'Metro', 0, 12, 'CAD', 18, 1),
(1642, '', 4.00, '2023-08-02', 'Provigo', 0, 12, 'CAD', 18, 1),
(1643, '', 16.50, '2023-08-03', 'Adonis', 0, 12, 'CAD', 18, 1),
(1644, '', 11.49, '2023-08-03', 'Spotify', 0, 20, 'CAD', 18, 1),
(1645, '', 4.25, '2023-08-04', 'Gatorade', 0, 5, 'CAD', 18, 1),
(1646, '', 20.70, '2023-08-05', 'AYLWIN BBQ', 0, 17, 'CAD', 18, 1),
(1647, '', 2.00, '2023-08-05', 'Air pump at gas station', 0, 9, 'CAD', 18, 1),
(1648, '', 8.00, '2023-08-07', 'Provigo Food (Escalope + pasta)', 0, 8, 'CAD', 18, 1),
(1649, '', 1000.00, '2023-08-08', 'Convert CAD to Euro', 0, 22, 'CAD', 18, 1),
(1650, '', 12.52, '2023-08-08', 'Metro', 0, 12, 'CAD', 18, 1),
(1651, '', 1415.85, '2023-08-08', 'Air Canada ticket', 0, 22, 'CAD', 18, 1),
(1652, '', 9.02, '2023-08-09', 'Shawarmaz', 0, 8, 'CAD', 18, 1),
(1653, '', 57.49, '2023-08-10', 'VIRGIN PLUS BPY', 0, 23, 'CAD', 18, 1),
(1654, '', 46.50, '2023-08-10', 'VIRGIN PLUS V', 0, 23, 'CAD', 18, 1),
(1655, '', 11.00, '2023-08-11', 'Airport Bus Ticket', 0, 22, 'CAD', 18, 1),
(1656, '', 30.63, '2023-08-14', 'LIME', 0, 22, 'CAD', 18, 1),
(1657, '', 30.54, '2023-08-17', 'LIME', 0, 22, 'CAD', 18, 1),
(1658, '', 1.28, '2023-08-17', 'LIME', 0, 22, 'CAD', 18, 1),
(1659, '', 346.64, '2023-08-17', 'ZARA', 0, 4, 'CAD', 18, 1),
(1660, '', 30.54, '2023-08-17', 'LIME', 0, 22, 'CAD', 18, 1),
(1661, '', 7.56, '2023-08-21', 'METRO', 0, 22, 'CAD', 18, 1),
(1662, '', 345.87, '2023-08-21', 'ZARA', 0, 4, 'CAD', 18, 1),
(1663, '', 670.00, '2023-08-21', 'Convert 500 USD to Euro', 0, 22, 'CAD', 18, 1),
(1664, '', 7.03, '2023-08-22', 'eSim for Nido', 0, 22, 'CAD', 18, 1),
(1665, '', 4.25, '2023-08-22', 'LIME', 0, 22, 'CAD', 18, 1),
(1666, '', 81.20, '2023-08-22', 'Communauto', 0, 21, 'CAD', 18, 1),
(1667, '', 11.00, '2023-08-22', 'Bus Ticket MTL Airport', 0, 22, 'CAD', 18, 1),
(1668, '', 6.43, '2023-08-22', 'McDonalds breakfast', 0, 8, 'CAD', 18, 1),
(1669, '', 34.46, '2023-08-27', '2 Brita Filiters', 0, 12, 'CAD', 18, 1),
(1670, '', 1.22, '2023-08-29', 'JEAN COUTU 250 _F', 0, 12, 'CAD', 18, 1),
(1671, '', 14.96, '2023-08-29', 'PROVIGO LE MARC _F', 0, 12, 'CAD', 18, 1),
(1672, 'SIAM CENTRE-VIL _F', 83.28, '2023-08-30', 'siam restaurant', 0, 17, 'CAD', 18, 1),
(1673, '', 3.00, '2023-08-30', 'USAT_TD710227 _F', 0, 9, 'CAD', 18, 1),
(1674, '', 13.09, '2023-08-31', 'METRO ETS 2416 _F', 0, 12, 'CAD', 18, 1),
(1675, '', 28.28, '2023-08-31', 'METRO ETS 2416 _F', 0, 12, 'CAD', 18, 1),
(1676, '', 13.22, '2023-08-31', 'Decathlon fix bike', 0, 9, 'CAD', 18, 1),
(1677, 'SEND E-TFR ***AAC', 460.00, '2023-10-23', 'Bota Bota spa', 0, 11, 'CAD', 18, 1),
(1678, 'LS 9159-6809 Qu   _F', 156.68, '2023-10-30', 'Onoir restaurant', 0, 17, 'CAD', 18, 1),
(1679, 'UBER CANADA/UBE   _V', 16.76, '2023-10-30', 'Uber taxi', 0, 21, 'CAD', 18, 1),
(1680, 'EUREST-43224      _F', 7.85, '2023-10-31', 'Morgan Stanley Cafeteria / fast food', 0, 8, 'CAD', 18, 1),
(1681, 'EUREST-43224      _F', 5.75, '2023-11-02', 'Morgan Stanley Cafeteria / fast food', 0, 8, 'CAD', 18, 1),
(1682, 'CANTEEN CANADA    _F', 3.74, '2023-11-02', 'Morgan Stanley vending machine / fast food', 0, 8, 'CAD', 18, 1),
(1683, '', 1300.00, '2023-11-04', 'Rent', 0, 14, 'CAD', 18, 1),
(1684, 'TD ATM W/D 000261', 20.00, '2023-11-04', 'Casino', 0, 7, 'CAD', 18, 1),
(1685, 'MCKIBBIN''S BISH _F', 64.37, '2023-11-04', 'McKibbin''s bar', 0, 7, 'CAD', 18, 1),
(1686, 'SALSATHEQUE _F', 41.00, '2023-11-04', 'SALSATHEQUE night club', 0, 7, 'CAD', 18, 1),
(1687, 'SIMLY 20.00_V', 28.37, '2023-11-06', 'Simly electronic sim', 0, 23, 'CAD', 18, 1),
(1688, 'METRO ETS 2416 _F', 17.76, '2023-11-07', 'Metro groceries', 0, 12, 'CAD', 18, 1),
(1689, 'LAINING ORIENTA _F', 31.00, '2023-11-07', 'china town souvenirs', 0, 14, 'CAD', 18, 1),
(1690, 'VIRGIN PLUS BPY', 31.00, '2023-11-07', 'virgin cellular', 0, 23, 'CAD', 18, 1),
(1691, 'FIVE GUYS BURGE _F', 25.48, '2023-11-07', 'five guys burger', 0, 8, 'CAD', 18, 1),
(1692, 'Spotify 12.64_V', 12.64, '2023-11-08', 'Spotify subscription', 0, 20, 'CAD', 18, 1),
(1693, 'HM St. Catherin _F', 76.54, '2023-11-08', 'H&M', 0, 4, 'CAD', 18, 1),
(1694, 'SHAWARMAZ PEEL _F', 34.05, '2023-11-09', 'SHAWARMAZ', 0, 8, 'CAD', 18, 1),
(1695, 'FIDO MOBILE      BPY', 40.77, '2023-01-09', 'phone', 0, 23, 'CAD', 18, 1),
(1696, 'VIRGIN PLUS      BPY', 57.49, '2023-01-10', '', 0, 23, 'CAD', 18, 1),
(1697, 'NAUTILUS PLUS -   _V', 22.98, '2023-01-13', 'gym', 0, 19, 'CAD', 18, 1),
(1698, 'MEA         100.00_V', 138.91, '2023-01-17', '', 0, 16, 'CAD', 18, 1),
(1699, 'HMSHost He   11.78_V', 11.78, '2023-01-17', '', 0, 16, 'CAD', 18, 1),
(1700, 'Amazon.ca         _V', 23.11, '2023-01-18', 'amazon', 0, 4, 'CAD', 18, 1),
(1701, 'PROVIGO LE MARC   _F', 14.36, '2023-01-18', 'provigo groceries', 0, 12, 'CAD', 18, 1),
(1702, 'PROVIGO LE MARC   _F', 25.40, '2023-01-18', '', 0, 12, 'CAD', 18, 1),
(1703, 'TOM-Burger T', 62.63, '2023-01-19', 'burger', 0, 17, 'CAD', 18, 1),
(1704, 'K2 PLUS BISTRO    _F', 34.36, '2023-01-20', 'k2 sushi', 0, 17, 'CAD', 18, 1),
(1705, 'PROVIGO LE MARC   _F', 72.70, '2023-01-23', '', 0, 12, 'CAD', 18, 1),
(1706, 'UPS STORE #344    _F', 58.65, '2023-01-23', '', 0, 16, 'CAD', 18, 1),
(1707, 'SEND E-TFR ***Hyz', 1300.00, '2023-01-23', 'Home Rent', 0, 14, 'CAD', 18, 1),
(1708, 'CANTOR            _F', 8.49, '2023-01-23', '', 0, 16, 'CAD', 18, 1),
(1709, 'SEND E-TFR ***6JD', 650.00, '2023-01-23', '', 0, 14, 'CAD', 18, 1),
(1710, 'SEND E-TFR ***Gj5', 250.00, '2023-01-23', '', 0, 14, 'CAD', 18, 1),
(1711, 'PETRO-CANADA      _F', 16.12, '2023-01-23', 'fuel', 0, 21, 'CAD', 18, 1),
(1712, 'SEND E-TFR ***Drz', 1700.00, '2023-01-23', '', 0, 14, 'CAD', 18, 1),
(1713, 'GYU-KAKU BBQ JA   _F', 34.57, '2023-01-23', 'gyu kaku restaurant', 0, 17, 'CAD', 18, 1),
(1714, '5498 MCGILL MCI   _F', 4.93, '2023-01-24', '', 0, 16, 'CAD', 18, 1),
(1715, 'UBER CANADA       _V', 25.81, '2023-01-24', '', 0, 21, 'CAD', 18, 1),
(1716, 'SEND E-TFR ***ZZX', 1.00, '2023-01-25', '', 0, 14, 'CAD', 18, 1),
(1717, 'SOUPE CAFE ET C   _F', 4.58, '2023-01-25', '', 0, 16, 'CAD', 18, 1),
(1718, 'PROVIGO LE MARC', 25.66, '2023-01-26', '', 0, 12, 'CAD', 18, 1),
(1719, 'NAUTILUS PLUS -   _V', 22.98, '2023-01-27', '', 0, 19, 'CAD', 18, 1),
(1720, 'PROVIGO LE MARC   _F', 60.38, '2023-01-30', '', 0, 12, 'CAD', 18, 1),
(1721, 'STM LOGE PEEL O   _F', 13.00, '2023-01-30', 'stm metro', 0, 21, 'CAD', 18, 1),
(1722, 'SALLE DE QUILLE', 48.40, '2023-01-30', '', 0, 7, 'CAD', 18, 1),
(1723, 'SALLE DE QUILLE', 13.25, '2023-01-30', 'bowling', 0, 7, 'CAD', 18, 1),
(1724, 'STM VERDUN DIN1', 3.50, '2023-01-30', 'stm metro', 0, 21, 'CAD', 18, 1),
(1725, 'STM LOGE LUCIEN   _F', 3.50, '2023-01-30', 'stm metro', 0, 21, 'CAD', 18, 1),
(1726, 'IKEA MONTREAL     _F', 11.19, '2023-01-30', 'ikea', 0, 14, 'CAD', 18, 1),
(1727, 'STM COTE VERTU', 3.50, '2023-01-30', 'stm  metro', 0, 21, 'CAD', 18, 1),
(1728, 'PROVIGO LE MARC   _F', 48.32, '2023-01-30', '', 0, 12, 'CAD', 18, 1),
(1729, 'PROVIGO LE MARC   _F', 6.18, '2023-01-30', '', 0, 12, 'CAD', 18, 1),
(1730, '5512 MCGILL MCC   _F', 15.26, '2023-01-31', '', 0, 16, 'CAD', 18, 1),
(1731, 'UBER CANADA       _V', 47.56, '2023-01-31', '', 0, 21, 'CAD', 18, 1),
(1732, 'PORTIONS          _F', 4.89, '2023-02-01', '', 0, 16, 'CAD', 18, 1),
(1733, 'CAP REIT          _F', 32.00, '2023-02-02', '', 0, 16, 'CAD', 18, 1),
(1734, 'COMPTOIR DU CHE   _F', 15.78, '2023-02-02', '', 0, 8, 'CAD', 18, 1),
(1735, 'METRO ETS  2416   _F', 49.63, '2023-02-02', '', 0, 12, 'CAD', 18, 1),
(1736, 'UBER* PENDING     _V', 11.49, '2023-02-03', 'uber', 0, 21, 'CAD', 18, 1),
(1737, 'METRO ETS  2416   _F', 51.19, '2023-02-03', '', 0, 12, 'CAD', 18, 1),
(1738, 'WWW.IKEA.CA       _V', 654.07, '2023-02-03', 'ikea', 0, 14, 'CAD', 18, 1),
(1739, 'AMZN Mktp CA      _V', 229.94, '2023-02-03', '', 0, 4, 'CAD', 18, 1),
(1740, 'AMZN Mktp CA      _V', 9.04, '2023-02-03', '', 0, 4, 'CAD', 18, 1),
(1741, 'AMZN Mktp CA      _V', 180.57, '2023-02-03', 'amazon', 0, 4, 'CAD', 18, 1),
(1742, 'DEPANNEUR NOORI   _F', 2.85, '2023-02-03', '', 0, 16, 'CAD', 18, 1),
(1743, 'UBER* TRIP        _V', 15.56, '2023-02-06', '', 0, 21, 'CAD', 18, 1),
(1744, 'STRUCTUBE', 1986.77, '2023-02-06', 'furniture', 0, 14, 'CAD', 18, 1),
(1745, 'STRUCTUBE         _F', 42.54, '2023-02-06', 'furniture', 0, 14, 'CAD', 18, 1),
(1746, 'UBER CANADA       _V', 12.55, '2023-02-06', '', 0, 21, 'CAD', 18, 1),
(1747, 'METRO ETS  2416   _F', 43.00, '2023-02-06', '', 0, 12, 'CAD', 18, 1),
(1748, 'PORTIONS          _F', 10.64, '2023-02-07', '', 0, 16, 'CAD', 18, 1),
(1749, 'METRO ETS  2416   _F', 2.16, '2023-02-07', '', 0, 12, 'CAD', 18, 1),
(1750, 'UBER* EATS PEND   _V', 20.96, '2023-02-07', '', 0, 10, 'CAD', 18, 1),
(1751, 'CHARCUTERIE LE    _F', 8.37, '2023-02-09', '', 0, 16, 'CAD', 18, 1),
(1752, 'FIDO MOBILE      BPY', 40.77, '2023-02-09', '', 0, 23, 'CAD', 18, 1),
(1753, 'NAUTILUS PLUS -   _V', 22.98, '2023-02-10', '', 0, 19, 'CAD', 18, 1),
(1754, 'PROVIGO LE MARC   _F', 10.17, '2023-02-10', '', 0, 12, 'CAD', 18, 1),
(1755, 'PAYPAL *AMAZEES   _V', 59.79, '2023-02-10', '', 0, 16, 'CAD', 18, 1),
(1756, 'VIRGIN PLUS      BPY', 57.49, '2023-02-10', '', 0, 23, 'CAD', 18, 1),
(1757, 'UBER* PENDING     _V', 16.91, '2023-02-13', '', 0, 21, 'CAD', 18, 1),
(1758, 'UBER* PENDING     _V', 0.10, '2023-02-13', '', 0, 21, 'CAD', 18, 1),
(1759, 'UBER* EATS PEND   _V', 21.62, '2023-02-13', 'uber eats', 0, 10, 'CAD', 18, 1),
(1760, 'PROVIGO LE MARC   _F', 6.88, '2023-02-13', '', 0, 12, 'CAD', 18, 1),
(1761, 'PROVIGO LE MARC', 81.06, '2023-02-14', '', 0, 12, 'CAD', 18, 1),
(1762, 'COMPTOIR DU CHE   _F', 29.42, '2023-02-14', 'comptoir du chef', 0, 8, 'CAD', 18, 1),
(1763, 'FLEURISTE CENTR   _F', 35.64, '2023-02-14', 'flowers', 0, 11, 'CAD', 18, 1),
(1764, 'STRUCTUBE         _F', 68.99, '2023-02-15', 'furniture', 0, 14, 'CAD', 18, 1),
(1765, 'COMPTOIR DU CHE   _F', 23.80, '2023-02-16', '', 0, 8, 'CAD', 18, 1),
(1766, 'COMPTOIR DU CHE   _F', 2.30, '2023-02-17', '', 0, 8, 'CAD', 18, 1),
(1767, 'TMCANADA    *RE   _V', 81.00, '2023-02-17', 'wwe', 0, 7, 'CAD', 18, 1),
(1768, 'UBER CANADA       _V', 16.30, '2023-02-17', '', 0, 21, 'CAD', 18, 1),
(1769, 'UBER CANADA       _V', 1.02, '2023-02-21', '', 0, 21, 'CAD', 18, 1),
(1770, 'UBER* EATS PEND   _V', 29.34, '2023-02-21', '', 0, 10, 'CAD', 18, 1),
(1771, 'SEND E-TFR ***9xE', 270.00, '2023-02-21', '', 0, 14, 'CAD', 18, 1),
(1772, 'Subway 24494      _F', 8.50, '2023-02-21', 'subway', 0, 8, 'CAD', 18, 1),
(1773, '5511 MCGILL RED   _F', 3.90, '2023-02-21', '', 0, 16, 'CAD', 18, 1),
(1774, 'MCDONALD''S #405   _F', 13.64, '2023-02-22', '', 0, 8, 'CAD', 18, 1),
(1775, 'SEND E-TFR ***sbk', 678.00, '2023-02-23', '', 0, 14, 'CAD', 18, 1),
(1776, 'NAUTILUS PLUS -   _V', 22.98, '2023-02-24', '', 0, 19, 'CAD', 18, 1),
(1777, 'METRO ETS  2416   _F', 20.62, '2023-02-24', '', 0, 12, 'CAD', 18, 1),
(1778, 'HYDRO-QUEBEC     BPY', 40.87, '2023-02-24', '', 0, 23, 'CAD', 18, 1),
(1779, 'METRO ETS  2416   _F', 23.67, '2023-02-27', '', 0, 12, 'CAD', 18, 1),
(1780, 'METRO ETS  2416   _F', 11.71, '2023-02-28', '', 0, 12, 'CAD', 18, 1),
(1781, 'UBER CANADA       _V', 32.78, '2023-03-01', '', 0, 21, 'CAD', 18, 1),
(1782, 'COMMUNAUTO        _V', 1.00, '2023-03-01', '', 0, 21, 'CAD', 18, 1),
(1783, 'Spotify      11.49_V', 11.49, '2023-03-03', '', 0, 20, 'CAD', 18, 1),
(1784, 'DELI PLANET', 40.00, '2023-03-03', 'comedy show', 0, 7, 'CAD', 18, 1),
(1785, 'DELI PLANET', 25.13, '2023-03-06', 'comedy show', 0, 8, 'CAD', 18, 1),
(1786, 'SEND E-TFR ***tN5', 194.00, '2023-03-06', '', 0, 14, 'CAD', 18, 1),
(1787, 'METRO ETS  2416   _F', 9.28, '2023-03-06', '', 0, 12, 'CAD', 18, 1),
(1788, 'UBER CANADA       _V', 20.66, '2023-03-06', '', 0, 21, 'CAD', 18, 1),
(1789, 'METRO ETS  2416   _F', 22.26, '2023-03-07', '', 0, 12, 'CAD', 18, 1),
(1790, 'AMZN Mktp CA      _V', 40.23, '2023-03-08', '', 0, 4, 'CAD', 18, 1),
(1791, 'COMPTOIR DU CHE   _F', 14.71, '2023-03-09', '', 0, 8, 'CAD', 18, 1),
(1792, 'COUCHE-TARD #13   _F', 4.59, '2023-03-09', '', 0, 5, 'CAD', 18, 1),
(1793, 'UBER CANADA       _V', 27.50, '2023-03-10', '', 0, 21, 'CAD', 18, 1),
(1794, 'NAUTILUS PLUS -   _V', 22.98, '2023-03-10', '', 0, 19, 'CAD', 18, 1),
(1795, 'SEND E-TFR ***pfR', 400.00, '2023-03-13', '', 0, 14, 'CAD', 18, 1),
(1796, 'UBER* PENDING     _V', 12.01, '2023-03-13', '', 0, 21, 'CAD', 18, 1),
(1797, 'UBER CANADA       _V', 23.33, '2023-03-13', '', 0, 21, 'CAD', 18, 1),
(1798, 'UBER* PENDING     _V', 0.91, '2023-03-13', '', 0, 21, 'CAD', 18, 1),
(1799, 'METRO ETS  2416   _F', 84.14, '2023-03-13', '', 0, 12, 'CAD', 18, 1),
(1800, 'SEND E-TFR ***8ku', 50.00, '2023-03-13', 'e-trasnfer', 0, 16, 'CAD', 18, 1),
(1801, 'SKI MONT SAINT-   _V', 174.76, '2023-03-13', 'ski', 0, 19, 'CAD', 18, 1),
(1802, 'PHARMAPRIX #193   _F', 10.39, '2023-03-13', '', 0, 18, 'CAD', 18, 1),
(1803, 'VIRGIN PLUS      BPY', 57.48, '2023-03-13', '', 0, 23, 'CAD', 18, 1),
(1804, 'FIDO MOBILE      BPY', 40.77, '2023-03-13', '', 0, 23, 'CAD', 18, 1),
(1805, 'METRO ETS  2416   _F', 6.89, '2023-03-14', '', 0, 12, 'CAD', 18, 1),
(1806, 'NSF PAID FEE', 5.00, '2023-03-14', '', 0, 16, 'CAD', 18, 1),
(1807, 'SEND E-TFR ***6jR', 25.00, '2023-03-14', '', 0, 14, 'CAD', 18, 1),
(1808, 'UBER* EATS PEND   _V', 32.64, '2023-03-14', '', 0, 10, 'CAD', 18, 1),
(1809, 'DANA-NRH PREMIE   _F', 3.09, '2023-03-16', '', 0, 16, 'CAD', 18, 1),
(1810, 'METRO ETS  2416   _F', 4.58, '2023-03-16', '', 0, 12, 'CAD', 18, 1),
(1811, 'METRO ETS  2416   _F', 26.64, '2023-03-20', '', 0, 12, 'CAD', 18, 1),
(1812, 'JOE''S PANINI      _F', 11.10, '2023-03-20', '', 0, 8, 'CAD', 18, 1),
(1813, 'UBER* PENDING     _V', 10.43, '2023-03-20', '', 0, 21, 'CAD', 18, 1),
(1814, 'STEVE MADDEN (S', 133.36, '2023-03-20', 'steve madden', 0, 4, 'CAD', 18, 1),
(1815, 'PROVIGO LE MARC   _F', 8.05, '2023-03-20', '', 0, 12, 'CAD', 18, 1),
(1816, 'UBER CANADA       _V', 9.26, '2023-03-20', '', 0, 21, 'CAD', 18, 1),
(1817, 'SEND E-TFR ***Bzn', 92.00, '2023-03-20', '', 0, 14, 'CAD', 18, 1),
(1818, 'UBER* PENDING     _V', 12.97, '2023-03-20', '', 0, 21, 'CAD', 18, 1),
(1819, 'HOT DOG MOBILE', 6.16, '2023-03-21', '', 0, 8, 'CAD', 18, 1),
(1820, 'COMMUNAUTO        _V', 149.63, '2023-03-22', 'communauto', 0, 21, 'CAD', 18, 1),
(1821, 'COMPTOIR DU CHE   _F', 14.96, '2023-03-23', '', 0, 8, 'CAD', 18, 1),
(1822, 'DEJEUNETTE        _F', 10.76, '2023-03-23', 'breakfast', 0, 8, 'CAD', 18, 1),
(1823, 'NON-TD ATM W/D', 228.00, '2023-03-23', '', 0, 16, 'CAD', 18, 1),
(1824, 'UBER* PENDING     _V', 12.77, '2023-03-23', '', 0, 21, 'CAD', 18, 1),
(1825, 'NAUTILUS PLUS -   _V', 22.98, '2023-03-24', '', 0, 19, 'CAD', 18, 1),
(1826, 'METRO ETS  2416   _F', 6.78, '2023-03-24', '', 0, 12, 'CAD', 18, 1),
(1827, 'EVENTBRITE/LATE   _V', 16.93, '2023-03-27', 'late', 0, 8, 'CAD', 18, 1),
(1828, 'DELI PLANET       _F', 15.18, '2023-03-27', 'deli', 0, 8, 'CAD', 18, 1),
(1829, 'LULU EPICERIE', 45.62, '2023-03-27', 'lulu', 0, 17, 'CAD', 18, 1),
(1830, 'UBER CANADA       _V', 38.19, '2023-03-27', '', 0, 21, 'CAD', 18, 1),
(1831, 'UBER CANADA       _V', 25.28, '2023-03-27', 'Reimbursement uber', 0, 21, 'CAD', 18, 1),
(1832, 'UBER* EATS PEND   _V', 19.86, '2023-03-27', '', 0, 10, 'CAD', 18, 1),
(1833, 'UBER CANADA       _V', 8.48, '2023-03-27', '', 0, 21, 'CAD', 18, 1),
(1834, 'HYDRO-QUEBEC     BPY', 21.57, '2023-03-28', '', 0, 23, 'CAD', 18, 1),
(1835, 'UBER* EATS PEND   _V', 19.54, '2023-03-29', '', 0, 10, 'CAD', 18, 1),
(1836, 'COMPTOIR DU CHE   _F', 15.74, '2023-03-30', '', 0, 8, 'CAD', 18, 1),
(1837, 'PROVIGO LE MARC   _F', 22.31, '2023-03-30', '', 0, 12, 'CAD', 18, 1),
(1838, 'OVERDRAFT INTEREST', 0.03, '2023-03-31', '', 0, 16, 'CAD', 18, 1),
(1839, 'OTHER BANK FEES', 2.00, '2023-03-31', '', 0, 9, 'CAD', 18, 1),
(1840, 'KETTLEMANS BAGE   _F', 33.87, '2023-04-03', 'kettlmans', 0, 8, 'CAD', 18, 1),
(1841, 'SEND E-TFR ***4y7', 1300.00, '2023-04-03', '', 0, 14, 'CAD', 18, 1),
(1842, 'KETTLEMANS BAGE   _F', 25.27, '2023-04-03', '', 0, 8, 'CAD', 18, 1),
(1843, 'Spotify      11.49_V', 11.49, '2023-04-03', '', 0, 20, 'CAD', 18, 1),
(1844, 'COUCHETARD #568   _F', 15.20, '2023-04-10', '', 0, 5, 'CAD', 18, 1),
(1845, 'PROVIGO LE MARC   _F', 44.27, '2023-04-10', '', 0, 12, 'CAD', 18, 1),
(1846, 'UBER CANADA       _V', 26.30, '2023-04-10', '', 0, 21, 'CAD', 18, 1),
(1847, 'SOLIT CAFE        _F', 20.80, '2023-04-10', 'cafe', 0, 8, 'CAD', 18, 1),
(1848, 'HOT DOG MOBILE', 6.16, '2023-04-10', 'mcgill hot dog', 0, 8, 'CAD', 18, 1),
(1849, 'UBER CANADA       _V', 36.98, '2023-04-10', '', 0, 21, 'CAD', 18, 1),
(1850, 'VIRGIN PLUS      BPY', 57.49, '2023-04-10', '', 0, 23, 'CAD', 18, 1),
(1851, 'FIDO MOBILE      BPY', 43.07, '2023-04-10', '', 0, 23, 'CAD', 18, 1),
(1852, 'AMIR              _F', 19.61, '2023-04-12', '', 0, 8, 'CAD', 18, 1),
(1853, 'METRO ETS  2416   _F', 11.48, '2023-04-12', '', 0, 12, 'CAD', 18, 1),
(1854, 'UBER* EATS PEND   _V', 28.76, '2023-04-13', '', 0, 10, 'CAD', 18, 1),
(1855, 'UBER CANADA       _V', 23.71, '2023-04-17', '', 0, 21, 'CAD', 18, 1),
(1856, 'PROVIGO LE MARC   _F', 17.74, '2023-04-17', '', 0, 12, 'CAD', 18, 1),
(1857, 'COUCHETARD #749   _F', 8.37, '2023-04-17', '', 0, 5, 'CAD', 18, 1),
(1858, 'IN *HASKOUR ACC   _V', 80.48, '2023-04-18', 'tax', 0, 9, 'CAD', 18, 1),
(1859, 'THEBAY.COM #196   _V', 215.58, '2023-04-19', 'la baie', 0, 4, 'CAD', 18, 1),
(1860, 'METRO ETS  2416   _F', 10.99, '2023-04-19', '', 0, 12, 'CAD', 18, 1),
(1861, 'UBER* EATS PEND   _V', 28.89, '2023-04-20', '', 0, 10, 'CAD', 18, 1),
(1862, 'COMMUNAUTO        _V', 57.28, '2023-04-21', '', 0, 21, 'CAD', 18, 1),
(1863, 'JOES PANINI', 11.10, '2023-04-24', 'joes panini', 0, 8, 'CAD', 18, 1),
(1864, 'PROVIGO LE MARC   _F', 18.37, '2023-04-24', '', 0, 12, 'CAD', 18, 1),
(1865, 'PIZZA DANY        _F', 5.28, '2023-04-24', 'danny pizza', 0, 8, 'CAD', 18, 1),
(1866, 'SEND E-TFR ***3vQ', 10.00, '2023-04-24', 'e-trasnfer', 0, 16, 'CAD', 18, 1),
(1867, 'UBER* EATS PEND   _V', 17.43, '2023-04-25', '', 0, 10, 'CAD', 18, 1),
(1868, 'UBER CANADA       _V', 38.73, '2023-04-25', '', 0, 21, 'CAD', 18, 1),
(1869, 'PROVIGO LE MARC   _F', 33.19, '2023-04-26', '', 0, 12, 'CAD', 18, 1),
(1870, 'METRO ETS  2416   _F', 32.72, '2023-04-27', '', 0, 12, 'CAD', 18, 1),
(1871, 'SQ *ENGINEERING   _F', 16.00, '2023-04-28', '', 0, 16, 'CAD', 18, 1),
(1873, 'SHO-DAN', 183.79, '2023-05-01', 'shodan', 0, 17, 'CAD', 18, 1),
(1874, 'SEND E-TFR ***gpv', 1300.00, '2023-05-02', '', 0, 14, 'CAD', 18, 1),
(1875, 'ESCONDITE         _F', 52.73, '2023-05-03', 'escondite', 0, 17, 'CAD', 18, 1),
(1876, 'METRO ETS  2416   _F', 18.23, '2023-05-03', '', 0, 12, 'CAD', 18, 1),
(1877, 'Spotify      11.49_V', 11.49, '2023-05-03', '', 0, 20, 'CAD', 18, 1),
(1878, 'MCGILL UNV   J6K3J3', 0.56, '2023-05-04', '', 0, 16, 'CAD', 18, 1),
(1879, 'METRO ETS  2416   _F', 30.09, '2023-05-04', '', 0, 12, 'CAD', 18, 1),
(1880, 'GASPARD           _V', 45.00, '2023-05-08', 'gaspard', 0, 17, 'CAD', 18, 1),
(1881, 'BURGER KING # 2   _V', 8.97, '2023-05-08', 'burger king', 0, 8, 'CAD', 18, 1),
(1882, 'METRO ETS  2416   _F', 12.99, '2023-05-08', '', 0, 12, 'CAD', 18, 1),
(1883, 'UBER CANADA       _V', 40.98, '2023-05-08', '', 0, 21, 'CAD', 18, 1),
(1884, 'METRO ETS  2416   _F', 39.67, '2023-05-08', '', 0, 12, 'CAD', 18, 1),
(1885, 'GARAGE BEIRUT     _F', 82.77, '2023-05-08', 'GARAGE BEIRUT', 0, 17, 'CAD', 18, 1),
(1886, 'METRO ETS  2416   _F', 6.43, '2023-05-08', '', 0, 12, 'CAD', 18, 1),
(1887, 'METRO ETS  2416   _F', 3.54, '2023-05-09', '', 0, 12, 'CAD', 18, 1),
(1888, 'FIDO MOBILE      BPY', 43.07, '2023-05-10', '', 0, 23, 'CAD', 18, 1),
(1889, 'WIENSTEIN & GAV', 33.52, '2023-05-11', 'w and g', 0, 17, 'CAD', 18, 1),
(1890, 'METRO ETS  2416   _F', 17.77, '2023-05-11', '', 0, 12, 'CAD', 18, 1),
(1891, 'VIRGIN PLUS      BPY', 57.49, '2023-05-11', '', 0, 23, 'CAD', 18, 1),
(1892, 'METRO ETS  2416   _F', 18.54, '2023-05-12', '', 0, 12, 'CAD', 18, 1),
(1893, 'METRO ETS  2416', 71.88, '2023-05-12', '', 0, 12, 'CAD', 18, 1),
(1894, 'UBER CANADA       _V', 12.06, '2023-05-15', '', 0, 21, 'CAD', 18, 1),
(1895, 'SOUBOIS', 29.88, '2023-05-15', 'soubois', 0, 7, 'CAD', 18, 1),
(1896, 'AMIR              _F', 12.86, '2023-05-15', 'amir', 0, 8, 'CAD', 18, 1),
(1897, 'CANCEL E-TFR FEE', 5.00, '2023-05-15', 'cancel e transfer', 0, 9, 'CAD', 18, 1),
(1898, 'SEND E-TFR ***trp', 70.00, '2023-05-15', '', 0, 14, 'CAD', 18, 1),
(1899, 'METRO ETS  2416   _F', 2.86, '2023-05-15', '', 0, 12, 'CAD', 18, 1),
(1900, 'METRO ETS  2416   _F', 11.78, '2023-05-16', '', 0, 12, 'CAD', 18, 1),
(1901, 'SEND E-TFR ***6GM', 12.00, '2023-05-16', '', 0, 14, 'CAD', 18, 1),
(1902, 'NON-TD ATM W/D', 62.50, '2023-05-17', 'atm', 0, 16, 'CAD', 18, 1),
(1903, 'METRO ETS  2416   _F', 12.99, '2023-05-17', '', 0, 12, 'CAD', 18, 1),
(1904, 'Amazon.ca Prime   _V', 113.83, '2023-05-17', '', 0, 4, 'CAD', 18, 1),
(1905, 'COUCHETARD #217   _F', 12.51, '2023-05-18', 'couchetard', 0, 5, 'CAD', 18, 1),
(1906, 'METRO ETS  2416   _F', 14.25, '2023-05-18', '', 0, 12, 'CAD', 18, 1),
(1907, 'SEND E-TFR ***Uvv', 120.00, '2023-05-19', 'e-transfer', 0, 16, 'CAD', 18, 1),
(1908, 'UBER CANADA       _V', 1.02, '2023-05-19', '', 0, 21, 'CAD', 18, 1),
(1909, 'MCDONALD''S #405   _F', 10.19, '2023-05-23', '', 0, 8, 'CAD', 18, 1),
(1910, 'DECATHLON MONTR   _F', 14.95, '2023-05-23', '', 0, 19, 'CAD', 18, 1),
(1911, 'DOMINOS PIZZA    _F', 31.40, '2023-05-23', 'dominos pizza', 0, 8, 'CAD', 18, 1),
(1912, 'METRO ETS  2416   _F', 16.24, '2023-05-23', '', 0, 12, 'CAD', 18, 1),
(1913, 'UBER CANADA       _V', 23.32, '2023-05-23', '', 0, 21, 'CAD', 18, 1),
(1914, 'COLLEGE TR    8.50_V', 11.89, '2023-05-23', '', 0, 16, 'CAD', 18, 1),
(1915, 'PROVIGO LE MARC   _F', 17.73, '2023-05-24', '', 0, 12, 'CAD', 18, 1),
(1916, 'PROVIGO LE MARC   _F', 91.05, '2023-05-24', '', 0, 12, 'CAD', 18, 1),
(1917, 'RESTAURANT SABR', 87.26, '2023-05-26', 'sabr resto', 0, 17, 'CAD', 18, 1),
(1918, 'METRO ETS  2416   _F', 16.33, '2023-05-26', '', 0, 12, 'CAD', 18, 1),
(1919, 'PROVIGO LE MARC   _F', 23.16, '2023-05-26', '', 0, 12, 'CAD', 18, 1),
(1920, 'PHARMAPRIX #193   _F', 34.46, '2023-05-26', 'pharmacy', 0, 18, 'CAD', 18, 1),
(1921, 'RESTAURANT SHAY   _F', 145.16, '2023-05-29', 'shay restaurant', 0, 17, 'CAD', 18, 1),
(1922, 'CHOCOLATS FAVOR', 15.16, '2023-05-29', '', 0, 16, 'CAD', 18, 1),
(1923, 'IMMIGRATION CAN   _V', 255.00, '2023-05-30', 'ircc pgwp', 0, 9, 'CAD', 18, 1),
(1924, 'OTHER BANK FEES', 2.00, '2023-05-31', 'bank fee', 0, 9, 'CAD', 18, 1),
(1925, '', 1300.00, '2023-06-01', 'Rent', 0, 14, 'CAD', 18, 1),
(1926, 'UBER CANADA       _V', 13.54, '2023-06-01', '', 0, 21, 'CAD', 18, 1),
(1927, 'UBER CANADA       _V', 24.88, '2023-06-02', '', 0, 21, 'CAD', 18, 1),
(1928, 'VIRGIN PLUS       _V', 120.11, '2023-06-02', '', 0, 23, 'CAD', 18, 1),
(1929, 'SEND E-TFR ***uNm', 104.00, '2023-06-02', '', 0, 14, 'CAD', 18, 1),
(1930, 'Spotify      11.49_V', 11.49, '2023-06-05', '', 0, 20, 'CAD', 18, 1),
(1931, 'AIR-SERV A PS60   _F', 2.00, '2023-06-05', '', 0, 16, 'CAD', 18, 1),
(1932, 'UBER CANADA       _V', 11.16, '2023-06-05', '', 0, 21, 'CAD', 18, 1),
(1933, 'UBER CANADA       _V', 10.08, '2023-06-05', '', 0, 21, 'CAD', 18, 1),
(1934, 'PROVIGO LE MARC   _F', 62.60, '2023-06-05', '', 0, 12, 'CAD', 18, 1),
(1935, 'UBER CANADA       _V', 13.18, '2023-06-05', '', 0, 21, 'CAD', 18, 1),
(1936, 'UBER CANADA       _V', 10.69, '2023-06-05', '', 0, 21, 'CAD', 18, 1),
(1937, 'UBER* PENDING     _V', 10.79, '2023-06-05', '', 0, 21, 'CAD', 18, 1),
(1938, 'METRO ETS  2416   _F', 26.11, '2023-06-07', '', 0, 12, 'CAD', 18, 1),
(1939, 'METRO ETS  2416   _F', 1.99, '2023-06-09', '', 0, 12, 'CAD', 18, 1),
(1940, 'FIDO MOBILE      BPY', 40.60, '2023-06-09', '', 0, 23, 'CAD', 18, 1),
(1941, 'CHUNGCHUN KOGO    _F', 16.45, '2023-06-12', 'chungchun', 0, 8, 'CAD', 18, 1),
(1942, 'UBER CANADA       _V', 12.25, '2023-06-12', '', 0, 21, 'CAD', 18, 1),
(1943, 'UBER CANADA       _V', 23.36, '2023-06-12', '', 0, 21, 'CAD', 18, 1),
(1944, 'SEND E-TFR ***u8C', 130.00, '2023-06-12', 'e-trasnfer', 0, 16, 'CAD', 18, 1),
(1945, 'SEND E-TFR ***xdq', 35.00, '2023-06-12', '', 0, 14, 'CAD', 18, 1),
(1946, 'UBER CANADA/UBE   _V', 74.04, '2023-06-12', '', 0, 21, 'CAD', 18, 1),
(1947, 'UBER* TRIP        _V', 13.01, '2023-06-12', 'uber', 0, 21, 'CAD', 18, 1),
(1948, 'NBX*ENSO YOGA I   _V', 34.49, '2023-06-12', 'enso yoga', 0, 18, 'CAD', 18, 1),
(1949, 'VIRGIN PLUS      BPY', 57.49, '2023-06-12', '', 0, 23, 'CAD', 18, 1),
(1950, 'STARBUCKS COFFE   _F', 6.03, '2023-06-13', 'starbucks', 0, 8, 'CAD', 18, 1),
(1951, 'COLLEGE TR    8.90_V', 12.33, '2023-06-13', '', 0, 16, 'CAD', 18, 1),
(1952, 'METRO ETS  2416   _F', 26.73, '2023-06-13', '', 0, 12, 'CAD', 18, 1),
(1953, 'CAMPO             _F', 41.97, '2023-06-13', 'campo', 0, 8, 'CAD', 18, 1),
(1954, 'DECATHLON MONTR   _F', 29.89, '2023-06-14', 'decathlon bike', 0, 19, 'CAD', 18, 1),
(1955, 'ZARA MONTREAL #', 255.27, '2023-06-16', 'zara', 0, 4, 'CAD', 18, 1),
(1956, 'GRIFF IN Self Care', 41.00, '2023-06-19', 'barber', 0, 18, 'CAD', 18, 1),
(1957, 'STM LUCIEN L AL', 13.00, '2023-06-19', 'stm metro', 0, 21, 'CAD', 18, 1),
(1958, 'AUBERGE SAINT-G   _F', 21.19, '2023-06-19', '', 0, 16, 'CAD', 18, 1),
(1959, 'UBER CANADA       _V', 1.15, '2023-06-19', '', 0, 21, 'CAD', 18, 1),
(1960, 'UBER CANADA/UBE   _V', 10.63, '2023-06-19', '', 0, 21, 'CAD', 18, 1),
(1961, 'SPA DIVA          _F', 11.49, '2023-06-19', 'spa diva', 0, 18, 'CAD', 18, 1),
(1962, 'JJ PLACE MONTRE', 112.68, '2023-06-19', 'jack and jones', 0, 4, 'CAD', 18, 1),
(1963, 'PROVIGO LE MARC   _F', 65.01, '2023-06-21', '', 0, 12, 'CAD', 18, 1),
(1964, 'METRO ETS  2416   _F', 10.78, '2023-06-22', '', 0, 12, 'CAD', 18, 1),
(1965, 'TERRASSE CARLA    _F', 21.71, '2023-06-22', 'terrasse carla', 0, 7, 'CAD', 18, 1),
(1966, 'UBER CANADA       _V', 13.64, '2023-06-23', '', 0, 21, 'CAD', 18, 1),
(1967, 'METRO ETS  2416', 13.98, '2023-06-23', '', 0, 12, 'CAD', 18, 1),
(1968, 'UBER CANADA       _V', 20.98, '2023-06-23', '', 0, 21, 'CAD', 18, 1),
(1969, 'METRO ETS  2416   _F', 7.58, '2023-06-26', '', 0, 12, 'CAD', 18, 1),
(1970, 'STM BONAVENTURE', 13.00, '2023-06-26', 'stm metro', 0, 21, 'CAD', 18, 1),
(1971, 'SQ *PIKNIC ELEC   _F', 14.95, '2023-06-26', 'piknic electronic', 0, 7, 'CAD', 18, 1),
(1972, 'MCDONALDS #405   _F', 26.17, '2023-06-26', 'mcdonalds', 0, 8, 'CAD', 18, 1),
(1973, 'SEND E-TFR ***aYy', 65.00, '2023-06-26', 'e-trasnfer', 0, 16, 'CAD', 18, 1),
(1974, 'BOBTECH ELECTRO', 172.46, '2023-06-27', 'fridge repair', 0, 14, 'CAD', 18, 1),
(1975, 'METRO ETS  2416   _F', 10.99, '2023-06-29', '', 0, 12, 'CAD', 18, 1),
(1976, 'METRO ETS  2416   _F', 10.10, '2023-06-30', '', 0, 12, 'CAD', 18, 1),
(1977, 'HYDRO-QUEBEC     BPY', 240.40, '2023-06-30', 'hydro quebec', 0, 23, 'CAD', 18, 1),
(1978, '', 10.00, '2023-11-05', 'Brunch', 0, 7, 'CAD', 18, 1),
(1979, '', 500.00, '2023-11-10', 'Money for nido in mtl', 0, 11, 'CAD', 18, 1),
(1980, 'MR PUFFS VIEUX _F', 11.45, '2023-11-10', 'mr puffs', 0, 8, 'CAD', 18, 1),
(1981, 'VIRGIN PLUS BPY', 57.50, '2023-11-10', 'VIRGIN PLUS wifi', 0, 23, 'CAD', 18, 1),
(1982, 'MONOPOLE _F', 42.30, '2023-11-11', 'monopole winebar', 0, 7, 'CAD', 18, 1),
(1983, 'metro ets 2416 _F', 11.23, '2023-11-12', 'metro', 0, 12, 'CAD', 18, 1),
(1984, 'SIAM CENTRE-VIL', 160.00, '2023-11-12', 'siam', 0, 17, 'CAD', 18, 1),
(1985, '', 26.00, '2023-11-14', 'H&M', 0, 11, 'CAD', 18, 1),
(1986, 'PIZZA LA NEW-YO _F', 13.80, '2023-11-15', 'pizza', 0, 8, 'CAD', 18, 1),
(1987, 'CAFE ABU EL ZUL _F', 58.20, '2023-11-15', 'cafe abu el zolf', 0, 17, 'CAD', 18, 1),
(1988, 'MONOPOLE _F', 25.13, '2023-11-16', 'monopole', 0, 7, 'CAD', 18, 1),
(1989, '', 31.00, '2023-11-17', '3 amigos', 0, 7, 'CAD', 18, 1),
(1990, 'RESTAURANT FISS _F', 102.00, '2023-11-18', 'sushi', 0, 17, 'CAD', 18, 1),
(1991, 'EPLV - BOUTIQUE _F', 14.00, '2023-11-18', 'botanical garden boutique', 0, 17, 'CAD', 18, 1),
(1992, 'STM LUCIEN L AL', 14.00, '2023-11-18', 'metro', 0, 21, 'CAD', 18, 1),
(1993, 'LULU EPICERIE _F', 20.00, '2023-11-20', 'lulu', 0, 17, 'CAD', 18, 1),
(1994, 'LULU EPICERIE _F', 6.50, '2023-11-20', 'lulu', 0, 17, 'CAD', 18, 1),
(1995, 'METRO ETS 2416 _F', 30.00, '2023-11-20', 'metro', 0, 12, 'CAD', 18, 1),
(1996, 'CAFE ABU EL ZUL _F', 37.00, '2023-11-20', 'cafe abu l zolof', 0, 17, 'CAD', 18, 1),
(1997, 'METRO ETS 2416 _F', 7.78, '2023-11-22', 'metro', 0, 12, 'CAD', 18, 1),
(1998, 'CHAUSSURES BROW', 170.00, '2023-11-22', 'BROWN shoes', 0, 4, 'CAD', 18, 1),
(1999, 'UBER CANADA/UBE _V', 41.00, '2023-11-23', 'uber eats', 0, 10, 'CAD', 18, 1),
(2000, 'HYDRO-QUEBEC BPY', 84.30, '2023-11-23', 'hydro quebec', 0, 23, 'CAD', 18, 1),
(2001, 'Uniqlo Canada P   _F', 34.38, '2023-11-24', 'Uniqlo', 0, 4, 'CAD', 18, 1),
(2002, 'Patisserie Mahr   _F', 22.89, '2023-11-24', 'Mahrousse', 0, 17, 'CAD', 18, 1),
(2003, 'STM LUCIEN L AL', 7.00, '2023-11-24', 'Stm metro', 0, 21, 'CAD', 18, 1),
(2004, 'PETRO CANADA135   _F', 45.98, '2023-11-24', 'Wine for pre', 0, 21, 'CAD', 18, 1),
(2005, 'METRO ETS  2416   _F', 48.86, '2023-11-27', 'Metro groceries', 0, 12, 'CAD', 18, 1),
(2006, 'TD ATM W/D    005965', 40.00, '2023-11-27', 'Notre barbier', 0, 18, 'CAD', 18, 1),
(2007, 'ESCONDITE VIEUX', 137.31, '2023-11-27', 'Escondite', 0, 17, 'CAD', 18, 1),
(2008, 'CICCIO            _F', 3.97, '2023-11-27', 'Ciccio cafe', 0, 17, 'CAD', 18, 1),
(2009, 'AIR FRANCE   62.00_V', 88.01, '2023-11-27', 'Air France baggage', 0, 11, 'CAD', 18, 1),
(2010, 'RESTAURANT BOUS   _F', 11.22, '2023-11-27', 'Boston', 0, 8, 'CAD', 18, 1),
(2011, 'MASSAGE EXPERTS   _F', 118.99, '2023-11-29', 'Massage', 0, 18, 'CAD', 18, 1),
(2012, 'BRASSERIE SOEUR   _F', 25.79, '2023-11-30', 'Bar', 0, 7, 'CAD', 18, 1),
(2013, 'METRO ETS  2416   _F', 29.06, '2023-12-01', '', 0, 12, 'CAD', 18, 1),
(2014, 'SIMLY         3.50_V', 4.94, '2023-12-01', 'simly', 0, 16, 'CAD', 18, 1),
(2015, 'PHARMACIE BABIN   _F', 16.64, '2023-12-01', 'medicine', 0, 18, 'CAD', 18, 1),
(2016, 'MAKAN SAJ         _F', 10.81, '2023-12-01', 'makan', 0, 8, 'CAD', 18, 1),
(2017, 'MAKAN SAJ         _F', 4.74, '2023-12-04', 'makan', 0, 8, 'CAD', 18, 1),
(2018, 'UBER CANADA/UBE   _V', 21.11, '2023-12-04', '', 0, 21, 'CAD', 18, 1),
(2019, 'STM SQUARE VICT', 3.75, '2023-12-04', 'stm metro', 0, 21, 'CAD', 18, 1),
(2020, 'NAZAR DONER KEB   _F', 16.63, '2023-12-04', 'kebab', 0, 8, 'CAD', 18, 1),
(2021, 'RESTAURANT LA F   _F', 50.24, '2023-12-04', 'bar la florida', 0, 7, 'CAD', 18, 1),
(2022, 'CANADA COLLEGE    _V', 205.00, '2023-12-04', 'french exam', 0, 9, 'CAD', 18, 1),
(2023, 'Spotify      12.64_V', 12.64, '2023-12-04', '', 0, 20, 'CAD', 18, 1),
(2024, 'SEND E-TFR ***37F', 11.00, '2023-12-04', '', 0, 16, 'CAD', 18, 1),
(2025, 'IGA 8093          _F', 4.59, '2023-12-05', 'pizza iga', 0, 8, 'CAD', 18, 1),
(2026, 'NEVSKI            _F', 40.99, '2023-12-06', 'bar', 0, 7, 'CAD', 18, 1),
(2027, 'ADONIS 21945 GR   _F', 9.09, '2023-12-07', 'potluck', 0, 8, 'CAD', 18, 1),
(2029, 'OBERSON', 172.41, '2023-12-08', 'Ski equipment', 0, 19, 'CAD', 18, 1),
(2030, 'WINNERS 340', 45.97, '2023-12-08', 'Ski equipment', 0, 19, 'CAD', 18, 1),
(2031, 'DECATHLON MONTR   _F', 118.42, '2023-12-08', '', 0, 19, 'CAD', 18, 1),
(2033, 'DOMAINE DU SKI _F', 63.00, '2023-12-09', 'Ski saint bruno', 0, 19, 'CAD', 18, 1),
(2034, 'MCDONALD''S #405 _F', 10.00, '2023-12-09', 'MCDONALD''S', 0, 8, 'CAD', 18, 1),
(2035, 'COMMUNAUTO        _V', 17.00, '2023-12-08', 'communauto for ski quipment', 0, 21, 'CAD', 18, 1),
(2036, 'COMMUNAUTO        _V', 24.00, '2023-12-09', 'communauto for ski trip', 0, 21, 'CAD', 18, 1),
(2037, 'KINTON RAMEN _F', 55.40, '2023-12-09', 'kinton ramen', 0, 17, 'CAD', 18, 1),
(2038, '', 1300.00, '2023-12-10', 'Rent', 0, 14, 'CAD', 18, 1),
(2039, 'VIRGIN PLUS BPY', 57.50, '2023-12-11', 'Virgin Wifi', 0, 23, 'CAD', 18, 1),
(2040, 'EUREST-43224      _F', 3.93, '2023-12-12', 'Cafeteria MS', 0, 8, 'CAD', 18, 1),
(2041, 'STM LOGE SQVICT   _F', 7.00, '2023-12-12', 'stm metro', 0, 21, 'CAD', 18, 1),
(2042, 'FENETRE SUR KAB   _F', 53.88, '2023-12-13', 'fenetre sur kaboul', 0, 17, 'CAD', 18, 1),
(2043, 'EUREST-43224      _F', 13.63, '2023-12-13', '', 0, 8, 'CAD', 18, 1),
(2044, 'EUREST-43224      _F', 3.02, '2023-12-13', '', 0, 8, 'CAD', 18, 1),
(2045, 'NEVSKI            _F', 11.90, '2023-12-13', '', 0, 7, 'CAD', 18, 1),
(2046, 'UBER CANADA/UBE   _V', 11.49, '2023-12-14', '', 0, 21, 'CAD', 18, 1),
(2047, 'SQ *LA LUTINERI', 26.44, '2023-12-14', 'Christmas Market coffee', 0, 7, 'CAD', 18, 1),
(2048, 'C.S. LONGUEUIL    _F', 12.40, '2023-12-15', 'Driving Test', 0, 9, 'CAD', 18, 1),
(2049, 'DISTRICT 5 SOCC', 25.00, '2023-12-15', '', 0, 19, 'CAD', 18, 1),
(2050, 'O FOUR            _F', 16.54, '2023-12-15', 'ofour', 0, 17, 'CAD', 18, 1),
(2051, 'MCDONALD''S #405 _F', 9.40, '2023-12-16', 'MCDONALD', 0, 8, 'CAD', 18, 1),
(2052, 'STM LUCIEN L AL', 7.00, '2023-12-16', 'stm metro', 0, 21, 'CAD', 18, 1),
(2053, 'WINNERS 340 _F', 51.70, '2023-12-16', 'WINNERS', 0, 11, 'CAD', 18, 1),
(2054, 'INDIGO 282 _F', 30.00, '2023-12-16', 'INDIGO', 0, 11, 'CAD', 18, 1),
(2055, 'GYUBEE JAPONAIS', 120.00, '2023-12-16', 'GYUBEE JAPONAIS', 0, 17, 'CAD', 18, 1),
(2056, '', 10.00, '2023-12-13', 'saq wine', 0, 7, 'CAD', 18, 1),
(2062, 'IGA 8093          _F', 17.50, '2023-12-19', 'groceries', 0, 12, 'CAD', 19, 1),
(2067, 'ADONIS 21945 GR   _F', 17.85, '2023-12-20', '', 0, 12, 'CAD', 19, 1),
(2071, 'UBER CANADA/UBE _V', 22.00, '2023-12-23', 'Uber Eats', 0, 10, 'CAD', NULL, 1),
(2070, 'METRO ETS 2416 _F', 56.17, '2023-12-24', '', 0, 12, 'CAD', NULL, 1),
(2072, 'MARCHE STANLEY _F', 13.00, '2023-12-23', 'Deppaneur cigs', 0, 5, 'CAD', NULL, 1),
(2073, 'HYDRO-QUEBEC BPY', 85.00, '2023-11-20', 'electricity', 0, 23, 'CAD', NULL, 1),
(2068, 'HYDRO-QUEBEC     BPY', 85.00, '2023-12-20', '', 0, 23, 'CAD', 19, 1),
(2032, 'VIRGIN PLUS      BPY', 46.52, '2023-12-08', 'phone', 0, 23, 'CAD', 18, 1),
(2086, 'METRO ETS 2416 _F', 46.50, '2023-12-27', 'Groceries', 0, 12, 'CAD', NULL, 1),
(2087, '', 16.00, '2023-12-27', 'cinema', 0, 7, 'CAD', NULL, 1),
(2088, 'UBER CANADA/UBE _V', 12.00, '2023-12-29', 'uber', 0, 21, 'CAD', NULL, 1),
(2089, 'CAFE SAINTLAURE _F', 10.30, '2023-12-29', '', 0, 7, 'CAD', NULL, 1),
(2092, 'DEPANNEUR LE KA _F', 18.30, '2023-12-30', 'le kahera', 0, 17, 'CAD', NULL, 1),
(2090, 'PATATI PATATA _F', 6.60, '2023-12-29', 'burger', 0, 8, 'CAD', NULL, 1),
(2091, 'SQ *3 MINOTS _F', 9.00, '2023-12-29', 'beer', 0, 7, 'CAD', NULL, 1),
(2093, 'CAFE ABU EL ZUL _F', 15.00, '2023-12-30', 'cafe', 0, 17, 'CAD', NULL, 1),
(2094, 'MORGAN STANLEY PAY', 1976.00, '2023-12-29', 'Salary', 0, 1, 'CAD', NULL, 1),
(2095, '', 1300.00, '2024-01-02', 'Rent', 0, 14, 'CAD', NULL, 1),
(2096, 'Spotify 12.64_V', 12.64, '2024-01-02', 'spotify', 0, 20, 'CAD', NULL, 1),
(2097, 'LS Tejano BBQ B _F', 20.00, '2024-01-03', 'tejano', 0, 8, 'CAD', NULL, 1),
(2098, '', 9.00, '2024-01-03', 'shawarma from metro', 0, 8, 'CAD', NULL, 1),
(2100, 'GST GST', 124.00, '2024-01-06', 'Tax', 0, 2, 'CAD', NULL, 1),
(2101, 'GIBBYS VIEUX MO _F', 66.00, '2024-01-05', 'gibbys', 0, 17, 'CAD', NULL, 1),
(2102, 'CP - HA MCGILL _F', 38.00, '2024-01-05', 'bar nihao', 0, 7, 'CAD', NULL, 1),
(2103, 'UBER* TRIP _V', 7.30, '2024-01-05', 'uber', 0, 21, 'CAD', NULL, 1),
(2099, 'UBER CANADA/UBE _V', 16.60, '2024-01-04', 'uber eats', 0, 10, 'CAD', NULL, 1),
(2121, 'UBER CANADA       _V', 11.25, '2024-01-12', '', 1, 3, 'CAD', 21, 1),
(2117, 'BRUTOPIA          _F', 21.09, '2024-01-10', 'bar food', 0, 17, 'CAD', 21, 1),
(2111, 'PlayStatio    3.79_V', 3.79, '2024-01-10', '', 0, 7, 'CAD', 21, 1),
(2120, 'BAM*APEX MARTIA   _V', 67.84, '2024-01-11', 'muay thai', 0, 19, 'CAD', 21, 1),
(2065, 'UBER CANADA/UBE   _V', 20.95, '2023-12-20', '', 1, 21, 'CAD', 19, 1),
(2061, 'UBER CANADA/UBE   _V', 19.18, '2023-12-18', '', 1, 21, 'CAD', 19, 1),
(2116, 'NEVSKI', 18.15, '2024-01-10', '', 1, 7, 'CAD', 21, 1),
(2110, 'CS *CASHSTAR GF   _V', 10.00, '2024-01-10', 'ps plus', 0, 7, 'CAD', 21, 1),
(2069, 'COMMUNAUTO        _V', 26.92, '2023-12-21', 'Nido to Airport', 0, 21, 'CAD', 19, 1),
(2134, 'SQ *ECORECREO     _F', 45.02, '2024-01-18', 'ice skating', 0, 7, 'CAD', 21, 1),
(2154, 'BAM*APEX MARTIA _V', 28.70, '2024-01-31', 'mouth guard', 0, 19, 'CAD', NULL, 1),
(2156, 'STM LOGE LUCIEN _F', 3.75, '2024-01-31', 'metro', 0, 21, 'CAD', NULL, 1),
(2157, 'STM EDOUARD MON', 3.75, '2024-01-31', 'metro', 0, 21, 'CAD', NULL, 1),
(2158, 'MCDONALD''S #405 _F', 10.00, '2024-01-31', '', 0, 8, 'CAD', NULL, 1),
(2159, 'Concordia BPY', 3241.63, '2024-01-31', 'Tuition for loulou', 0, 11, 'CAD', NULL, 1),
(2162, 'E-TRANSFER ***3Ef', 11.00, '2024-02-01', '', 1, 3, 'CAD', 23, 1),
(2128, 'Bromont Montagn   _F', 14.38, '2024-01-15', 'Food bromont', 0, 17, 'CAD', 21, 1),
(2123, 'MORGAN STANLEY   PAY', 2021.16, '2024-01-15', '', 1, 1, 'CAD', 21, 1),
(2129, 'Bromont Montagn   _F', 14.66, '2024-01-15', '', 1, 17, 'CAD', 21, 1),
(2133, 'SQ *ECORECREO     _F', 36.01, '2024-01-16', '', 1, 7, 'CAD', 21, 1),
(2132, 'EUREST-43224      _F', 2.27, '2024-01-16', '', 1, 8, 'CAD', 21, 1),
(2130, 'UBER CANADA/UBE   _V', 11.49, '2024-01-15', '', 1, 21, 'CAD', 21, 1),
(2126, 'PROVIGO LE MARC   _F', 26.78, '2024-01-15', '', 1, 12, 'CAD', 21, 1),
(2125, 'UBER CANADA/UBE   _V', 16.35, '2024-01-15', '', 1, 21, 'CAD', 21, 1),
(2124, 'UBER CANADA/UBE   _V', 24.80, '2024-01-15', '', 1, 21, 'CAD', 21, 1),
(2122, 'STM LUCIEN L AL', 14.00, '2024-01-12', '', 1, 21, 'CAD', 21, 1),
(2118, 'VIRGIN PLUS      BPY', 57.49, '2024-01-10', '', 1, 23, 'CAD', 21, 1),
(2115, 'EUREST-43224      _F', 4.12, '2024-01-10', '', 1, 8, 'CAD', 21, 1),
(2108, 'VIRGIN PLUS      BPY', 46.52, '2024-01-08', '', 1, 23, 'CAD', 21, 1),
(2107, 'METRO ETS  2416   _F', 49.28, '2024-01-08', '', 1, 12, 'CAD', 21, 1),
(2106, 'UBER* TRIP        _V', 7.32, '2024-01-08', '', 1, 21, 'CAD', 21, 1),
(2113, 'UBER CANADA/UBE   _V', 23.66, '2024-01-10', '', 0, 12, 'CAD', 21, 1),
(2135, 'METRO ETS 2416 _F', 55.00, '2024-01-20', 'metro groceries', 0, 12, 'CAD', NULL, 1),
(2136, 'CP - HA MCGILL _F', 43.00, '2024-01-19', 'nhao bar', 0, 7, 'CAD', NULL, 1),
(2137, 'DOUBLETREE BY H', 126.00, '2024-01-19', 'bivouac', 0, 17, 'CAD', NULL, 1),
(2138, '', 30.00, '2024-01-20', 'uber', 0, 21, 'CAD', NULL, 1),
(2139, 'DISPENSA EPICER _F', 17.50, '2024-01-22', '', 0, 8, 'CAD', NULL, 1),
(2140, 'DISPENSA EPICER _F', 12.50, '2024-01-23', '', 0, 8, 'CAD', NULL, 1),
(2142, 'BAM*APEX MARTIA _V', 68.00, '2024-01-25', 'MMA', 0, 19, 'CAD', NULL, 1),
(2143, 'CAFE MADHATTER _F', 10.00, '2024-01-25', 'madhatterz', 0, 7, 'CAD', NULL, 1),
(2144, 'COMMUNAUTO        _V', 20.00, '2023-12-15', 'Communauto to Football And Driving Test', 0, 21, 'CAD', NULL, 1),
(2145, '', 20.00, '2024-01-25', 'E-transfer for ski to Bromont Jan 15', 0, 21, 'CAD', NULL, 1),
(2146, 'COMMUNAUTO        _V', 30.00, '2024-01-15', 'cancelled communauto', 0, 21, 'CAD', NULL, 1),
(2147, 'ROCKABERRY GRIF _F', 40.00, '2024-01-26', 'Cake for sultan', 0, 11, 'CAD', NULL, 1),
(2148, 'PIZZA PIZZA # 3 _F', 26.00, '2024-01-26', '', 0, 10, 'CAD', NULL, 1),
(2149, '', 75.00, '2024-01-26', 'Still life', 0, 7, 'CAD', NULL, 1),
(2150, 'PADELSPORT - MT _F', 31.60, '2024-01-29', '', 0, 19, 'CAD', NULL, 1),
(2151, 'SHAWARMAZ PEEL _F', 9.76, '2024-01-29', '', 0, 8, 'CAD', NULL, 1),
(2153, 'MORGAN STANLEY PAY', 2236.00, '2024-01-31', '', 0, 1, 'CAD', NULL, 1),
(2152, 'ADONIS 21945 GR _F', 11.00, '2024-01-30', 'food => 33/3', 0, 12, 'CAD', NULL, 1),
(2155, 'DEPANNEUR NOORI _F', 10.00, '2024-01-31', '', 0, 5, 'CAD', NULL, 1),
(2188, 'VIRGIN PLUS      BPY', 57.49, '2024-02-12', '', 1, 23, 'CAD', 23, 1),
(2187, 'PROVIGO LE MARC   _F', 8.05, '2024-02-12', '', 1, 12, 'CAD', 23, 1),
(2186, 'METRO ETS  2416   _F', 54.40, '2024-02-12', '', 1, 12, 'CAD', 23, 1),
(2185, 'PlayStatio   13.79_V', 13.79, '2024-02-12', '', 1, 7, 'CAD', 23, 1),
(2179, 'BAM*APEX MARTIA   _V', 67.84, '2024-02-08', '', 1, 19, 'CAD', 23, 1),
(2178, 'VIRGIN PLUS      BPY', 46.59, '2024-02-07', '', 1, 23, 'CAD', 23, 1),
(2177, 'UBER CANADA/UBE   _V', 9.33, '2024-02-07', '', 1, 21, 'CAD', 23, 1),
(2176, 'CANTEEN CANADA    _F', 3.74, '2024-02-07', '', 1, 8, 'CAD', 23, 1),
(2173, 'PROVIGO LE MARC   _F', 5.75, '2024-02-05', '', 1, 12, 'CAD', 23, 1),
(2170, 'Spotify      12.64_V', 12.64, '2024-02-05', '', 1, 20, 'CAD', 23, 1),
(2169, 'SEND E-TFR ***mfw', 15.00, '2024-02-05', '', 1, 14, 'CAD', 23, 1),
(2168, 'GYUBEE JAPONAIS   _F', 120.30, '2024-02-05', '', 1, 17, 'CAD', 23, 1),
(2165, 'PADELSPORT - MT   _F', 31.62, '2024-02-02', '', 1, 19, 'CAD', 23, 1),
(2163, 'PROVIGO LE MARC   _F', 53.10, '2024-02-01', '', 1, 12, 'CAD', 23, 1),
(2184, 'SEND E-TFR ***BYX', 17.00, '2024-02-09', 'Monopole to thomas', 0, 7, 'CAD', 23, 1),
(2182, 'UBER CANADA/UBE   _V', 19.89, '2024-02-08', '', 0, 10, 'CAD', 23, 1),
(2180, 'HEROKU* JA    6.00_V', 8.38, '2024-02-08', 'heorku bud man', 0, 9, 'CAD', 23, 1),
(2174, 'AMZN Mktp CA      _V', 24.22, '2024-02-06', 'Protein shake', 0, 12, 'CAD', 23, 1),
(2175, 'PIZZERIA NO.900   _F', 64.90, '2024-02-06', '', 0, 17, 'CAD', 23, 1),
(2167, 'SEND E-TFR ***V5P', 1300.00, '2024-02-02', 'Rent', 0, 14, 'CAD', 23, 1),
(2172, 'GRILLADES POULE   _F', 17.86, '2024-02-05', 'Poulet rouge', 0, 8, 'CAD', 23, 1),
(2166, 'MORGAN STANLEY   PAY', 898.69, '2024-02-02', 'bonus', 0, 1, 'CAD', 23, 1),
(2161, 'MCDONALD''S #405   _F', 10.08, '2024-02-01', '', 1, 8, 'CAD', 23, 1),
(2160, 'STM EDOUARD MON', 3.75, '2024-02-01', '', 1, 21, 'CAD', 23, 1),
(2192, 'FONDATION SAINT   _V', 25.00, '2024-02-13', '', 1, 16, 'CAD', 24, 1),
(2195, 'MORGAN STANLEY   PAY', 2127.55, '2024-02-15', '', 1, 1, 'CAD', 24, 1),
(2200, 'E-TRANSFER ***XSf', 40.00, '2024-02-20', '', 1, 2, 'CAD', 24, 1),
(2201, 'METRO ETS  2416   _F', 38.03, '2024-02-20', '', 1, 12, 'CAD', 24, 1),
(2194, 'PROVIGO LE MARC   _F', 36.08, '2024-02-14', '', 1, 12, 'CAD', 24, 1),
(2191, 'AMZN Mktp CA      _V', 12.95, '2024-02-13', '', 1, 4, 'CAD', 24, 1),
(2190, 'SEND E-TFR ***3k5', 26.00, '2024-02-13', '', 1, 14, 'CAD', 24, 1),
(2189, 'PADELSPORT - MT   _F', 5.75, '2024-02-13', '', 1, 19, 'CAD', 24, 1),
(2199, 'CORP. SKI & GOL   _V', 57.49, '2024-02-20', 'Orford Ski', 0, 19, 'CAD', 24, 1),
(2196, 'RESTAURANT GRIN', 204.94, '2024-02-15', 'GRINDR Valentine', 0, 17, 'CAD', 24, 1),
(2193, 'FLEURISTE BOTAN   _F', 28.74, '2024-02-14', 'flowers valentin', 0, 11, 'CAD', 24, 1),
(2216, 'GYU-KAKU BBQ JA _F', 65.84, '2024-02-21', '', 1, 17, 'CAD', 27, 1),
(2215, 'STM LUCIEN L AL', 7.00, '2024-02-21', '', 1, 21, 'CAD', 27, 1),
(2214, 'BAM*APEX MARTIA _V', 67.84, '2024-02-22', '', 1, 19, 'CAD', 27, 1),
(2213, 'EUREST-43224 _F', 12.87, '2024-02-22', '', 1, 8, 'CAD', 27, 1),
(2212, 'HYDRO-QUEBEC BPY', 334.64, '2024-02-22', '', 1, 23, 'CAD', 27, 1),
(2211, 'METRO ETS 2416 _F', 21.07, '2024-02-23', '', 1, 12, 'CAD', 27, 1),
(2210, 'STM LUCIEN L AL', 7.00, '2024-02-23', '', 1, 21, 'CAD', 27, 1),
(2204, 'UBER* EATS _V', 38.26, '2024-02-24', '', 1, 10, 'CAD', 27, 1),
(2203, 'UBER CANADA/UBE _V', 9.27, '2024-02-25', '', 1, 21, 'CAD', 27, 1),
(2205, '', 27.00, '2024-02-25', 'Padel', 0, 19, 'CAD', 27, 1),
(2208, 'BILLIARD FATS _F', 9.90, '2024-02-23', 'bar', 0, 7, 'CAD', 27, 1),
(2207, 'OSMOW''S MONTREA _F', 11.14, '2024-02-23', '', 0, 8, 'CAD', 27, 1),
(2206, '', 40.00, '2024-02-24', 'Notre barbier', 0, 18, 'CAD', 27, 1),
(2209, 'C.S. HENRI-BOUR _F', 12.80, '2024-02-23', 'Driving test', 0, 9, 'CAD', 27, 1),
(2198, 'CORP. SKI & GOL   _F', 4.00, '2024-02-20', 'Orford Parking => 16 / 4', 0, 9, 'CAD', 24, 1),
(2197, 'TIM HORTONS #37   _F', 10.00, '2024-02-20', '38 / 4', 0, 8, 'CAD', 24, 1)
;

--
-- PostgreSQL database dump complete
--

COMMIT;