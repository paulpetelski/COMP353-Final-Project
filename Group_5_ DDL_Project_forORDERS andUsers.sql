Insert into Orders
(OrderID, CustomerID, DateOfOrder, ShippingDate, UserEmail)  
values 
(0, 5, '2021-01-05', '2021-01-07', 'alexis@gmail.com'), 
(1, 6, '2021-03-07', '2021-03-09', 'melissa@gmail.com'),
(2, 4, '2021-04-10', '2021-04-12', 'alison@gmail.com'), 
(3, 14, '2021-05-14', '2021-05-16', 'joanna@gmail.com'), 
(4, 10, '2021-12-21', '2021-12-23', 'samantha@gmail.com'), 
(5, 1, '2021-12-26', '2021-12-28', 'amanda@gmail.com'),
(6, 1, '2022-01-10', '2022-01-12', 'amanda@gmail.com'),
(7, 14, '2022-01-10', '2022-01-12', 'joanna@gmail.com'),
(8, 2, '2022-01-12', '2022-01-12', 'corey@gmail.com');

 Insert into OrderLine
 (OrderID, ProductID, Quantity, SubscriptionStartDate, SubscriptionEndDate) 
 Values 
 (0, 13, 2, '2021-01-05', '2022-01-05'), 
 (1, 1, 4, Null, Null), 
 (2, 9, 1, Null, Null), 
 (3, 12, 1, '2021-05-14', '2023-05-14'), 
 (4, 12, 1, '2021-12-21', '2023-12-21'),
 (5, 6, 1, Null, Null),  
 (5, 13, 3,'2021-12-26', '2022-12-26'),
 (6, 15, 1, '2022-01-10', '2024-01-10'),
 (6, 4, 2, Null, Null ),
 (7, 10, 1,Null, Null ),
 (7, 0, 2, Null, Null ),
 (7, 14, 1,'2022-01-10','2024-01-10'),
 (8, 2, 1, Null, Null);

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(0, 'Admin', 'admin@gmail.com', '$2b$12$rg2VMfMpW81lXeuZwD6vcOnmaQMC64upxwfoDj3mMzn8XTo4WY5sK'),
(1, 'Amanda', 'amanda@gmail.com', '$2b$12$XCpzX8Ds/17lM6VcxaAdkeUikpZ0aSCSa/kh0Br2STpbDHBlIhpdu'),
(2, 'Corey', 'corey@gmail.com', '$2b$12$s.Brfxf9sQdlbHbu9.dkleBigtHi2n8ZsCwFfmlCgSCJK4.0m7jLm'),
(3, 'Matthew', 'matthew@gmail.com', '$2b$12$ojHQeA.kcf4MiMd8xmB.zeMRaLXOsB.uiLohrqFvcPvZrGjyhjfuC'),
(4, 'Alison', 'alison@gmail.com', '$2b$12$D1Yy/t.DuwHRDoKhclKYc.v6q.t905rVfu8Bz9KXRVbAuVllZrKrG'),
(5, 'Alexis', 'alexis@gmail.com', '$2b$12$LTfgn8lJVTNKpjUr3KFaD.exes7rAIu82Ra5YzF1SOp2s9.RQB4jG'),
(6, 'Melissa', 'melissa@gmail.com', '$2b$12$nckg5U5thFjRoif0yU9iCeC6WQ2T26sfO2QrwtTY0ybGZ0l3OekOu'),
(7, 'Crystal', 'crystal@gmail.com', '$2b$12$1odoSmS.bf.V/hHL73XM7.kwDq3/x4XSpu.6aMUjfXIJXd7gG7Pqa'),
(8, 'Christine', 'christine@gmail.com', '$2b$12$jL4nNAk5zG5geKtixXdAauhcP0nTuwJQiRtJsDR5Q8.5mxN1ZzfEm'),
(9, 'Dominique', 'dominique@gmail.com', '$2b$12$ayMQUMMY4ypdmoT9ssgFKOABgFO/pxq/c11lYZNPjZdudsFy2RZ5m'),
(10, 'Samantha', 'samantha@gmail.com', '$2b$12$4zOwA/1mE73Rnzng3S29IOCeZBKe3bCl6dEbzAfyi.zqnnIAdMHHq'),
(11, 'Gabriela', 'gabriela@gmail.com', '$2b$12$Mu5s0UXkp4dsIMOwTXXySe8H1HIvXyj8Nj4XE1Sfx0mM.uRihAFUO'),
(12, 'Marie', 'marie@gmail.com', '$2b$12$ZVdR4P8JU9QeC3Z8IGRTeuSyWBtdJ0sbfPpOPsyqzi20F0oUSFuXW'),
(13, 'Nicholas', 'nicholas@gmail.com', '$2b$12$0o5n.hVHPcHcVuTXGMzFwuAXpaP30d4Uxy4S.ylNRo7fSIRL7EMUa'),
(14, 'Joanna', 'joanna@gmail.com', '$2b$12$.P2mRhnZV.byRwxWgB3WIOnw2/xT4qSK29/VFfbvxfVl06sc41g.e');
