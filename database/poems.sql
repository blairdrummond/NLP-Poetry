CREATE TABLE Poets (
       firstname  varchar(50),
       middlename varchar(50),
       lastname   varchar(50),
       birthyear  integer,
       deathyear  integer,

       CONSTRAINT poet_pkey      PRIMARY KEY (firstname, middlename, lastname),

       CONSTRAINT anonymous_poet CHECK ((firstname =  'Anonymous' AND lastname =  'Anonymous')
				      		   	          OR
		                        (firstname != 'Anonymous' AND lastname != 'Anonymous'))
);


CREATE TABLE Poems (
       pname  	    varchar(200),
       poet_f_name  varchar(50),
       poet_m_name  varchar(50), 
       poet_l_name  varchar(50),
       region	    varchar(50) NULL,
       subregion    varchar(50) NULL,
       number       integer,

       CONSTRAINT poem_pkey PRIMARY KEY (pname, poet_f_name, poet_m_name, poet_l_name),

       CONSTRAINT poet_fkey FOREIGN KEY (poet_f_name, poet_m_name, poet_l_name) REFERENCES Poets
);

CREATE TABLE Categories (
       category	    varchar(50),
       
       CONSTRAINT category_pkey PRIMARY KEY (category)
);

CREATE TABLE HasCategories (
       pname  	    varchar(200),
       poet_f_name  varchar(50),
       poet_m_name  varchar(50), 
       poet_l_name  varchar(50),
       category     varchar(50),

       CONSTRAINT no_duplicates UNIQUE (pname, poet_f_name, poet_m_name, poet_l_name, category),

       CONSTRAINT poem_fkey	FOREIGN KEY (pname, 
       		  			     poet_f_name,
					     poet_m_name, 
					     poet_l_name) REFERENCES Poems,

       CONSTRAINT category_fkey FOREIGN KEY (category)    REFERENCES Categories
);
