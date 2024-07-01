-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema new_forum_project
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema new_forum_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `new_forum_project` DEFAULT CHARACTER SET latin1 ;
USE `new_forum_project` ;

-- -----------------------------------------------------
-- Table `new_forum_project`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_forum_project`.`category` (
  `name_of_category` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`name_of_category`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `new_forum_project`.`new_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_forum_project`.`new_user` (
  `id_of_user` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(60) NOT NULL,
  `nickname` VARCHAR(40) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  `gender` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id_of_user`))
ENGINE = InnoDB
AUTO_INCREMENT = 21
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `new_forum_project`.`conversations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_forum_project`.`conversations` (
  `id_of_conversations` INT(11) NOT NULL AUTO_INCREMENT,
  `the_receiver` INT(11) NOT NULL,
  `the_sender` INT(11) NOT NULL,
  PRIMARY KEY (`id_of_conversations`),
  INDEX `fk_conversations_new_user1_idx` (`the_receiver` ASC) VISIBLE,
  INDEX `fk_conversations_new_user2_idx` (`the_sender` ASC) VISIBLE,
  CONSTRAINT `fk_conversations_new_user1`
    FOREIGN KEY (`the_receiver`)
    REFERENCES `new_forum_project`.`new_user` (`id_of_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_conversations_new_user2`
    FOREIGN KEY (`the_sender`)
    REFERENCES `new_forum_project`.`new_user` (`id_of_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `new_forum_project`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_forum_project`.`messages` (
  `id_of_messages` INT(11) NOT NULL AUTO_INCREMENT,
  `text_message` TEXT NOT NULL,
  `conversation_id` INT(11) NOT NULL,
  `the_sender` INT(11) NOT NULL,
  PRIMARY KEY (`id_of_messages`),
  INDEX `fk_messages_conversations_between_users1_idx` (`conversation_id` ASC) VISIBLE,
  INDEX `fk_messages_new_user1_idx` (`the_sender` ASC) VISIBLE,
  CONSTRAINT `fk_messages_conversations_between_users1`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `new_forum_project`.`conversations` (`id_of_conversations`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_new_user1`
    FOREIGN KEY (`the_sender`)
    REFERENCES `new_forum_project`.`new_user` (`id_of_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 20
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `new_forum_project`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_forum_project`.`replies` (
  `id_of_replies` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `new_topic_id` INT(11) NOT NULL,
  `new_user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id_of_replies`),
  INDEX `fk_replies_new_topic1_idx` (`new_topic_id` ASC) VISIBLE,
  INDEX `fk_replies_new_user1_idx` (`new_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_new_topic1`
    FOREIGN KEY (`new_topic_id`)
    REFERENCES `new_forum_project`.`new_topic` (`id_of_topic`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_new_user1`
    FOREIGN KEY (`new_user_id`)
    REFERENCES `new_forum_project`.`new_user` (`id_of_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `new_forum_project`.`new_topic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_forum_project`.`new_topic` (
  `id_of_topic` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `topic_text` LONGTEXT NOT NULL,
  `date_of_creation` DATETIME NOT NULL,
  `category_name_of_category` VARCHAR(25) NOT NULL,
  `id_of_author` INT(11) NOT NULL,
  `best_reply_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id_of_topic`),
  INDEX `fk_new_topic_category1_idx` (`category_name_of_category` ASC) VISIBLE,
  INDEX `fk_new_topic_new_user1_idx` (`id_of_author` ASC) VISIBLE,
  INDEX `fk_new_topic_replies1_idx` (`best_reply_id` ASC) VISIBLE,
  CONSTRAINT `fk_new_topic_category1`
    FOREIGN KEY (`category_name_of_category`)
    REFERENCES `new_forum_project`.`category` (`name_of_category`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_new_topic_new_user1`
    FOREIGN KEY (`id_of_author`)
    REFERENCES `new_forum_project`.`new_user` (`id_of_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_new_topic_replies1`
    FOREIGN KEY (`best_reply_id`)
    REFERENCES `new_forum_project`.`replies` (`id_of_replies`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 20
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `new_forum_project`.`reactions_of_replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_forum_project`.`reactions_of_replies` (
  `id_of_likes` INT(11) NOT NULL AUTO_INCREMENT,
  `UpVote` INT(11) NULL DEFAULT NULL,
  `DownVote` INT(11) NULL DEFAULT NULL,
  `new_user_id` INT(11) NOT NULL,
  `id_of_replies` INT(11) NOT NULL,
  PRIMARY KEY (`id_of_likes`),
  INDEX `fk_likes_of_post_new_user1_idx` (`new_user_id` ASC) VISIBLE,
  INDEX `fk_reactions_of_post_replies1_idx` (`id_of_replies` ASC) VISIBLE,
  CONSTRAINT `fk_likes_of_post_new_user1`
    FOREIGN KEY (`new_user_id`)
    REFERENCES `new_forum_project`.`new_user` (`id_of_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reactions_of_post_replies1`
    FOREIGN KEY (`id_of_replies`)
    REFERENCES `new_forum_project`.`replies` (`id_of_replies`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;








-- -----------------------------------------------------------------------------
-- The following code is intended for populating the database with information.
-- -----------------------------------------------------------------------------



ALTER TABLE new_forum_project.category AUTO_INCREMENT = 1;
ALTER TABLE new_forum_project.new_user AUTO_INCREMENT = 1;
ALTER TABLE new_forum_project.new_topic AUTO_INCREMENT = 1;
ALTER TABLE new_forum_project.replies AUTO_INCREMENT = 1;
ALTER TABLE new_forum_project.messages AUTO_INCREMENT = 1;
ALTER TABLE new_forum_project.conversations AUTO_INCREMENT = 1;
ALTER TABLE new_forum_project.reactions_of_replies AUTO_INCREMENT = 1;




-- 1. CATEGORY
INSERT INTO new_forum_project.category (name_of_category)
VALUE ('Fitness'), ('Football'), ('Volleyball');
-- -----------------------------------------------------------------------------



-- 2. USERS
INSERT INTO new_forum_project.new_user (email, nickname, password, date_of_birth, gender)
VALUES
    ('boris@gmail.com', 'boris', '123321', '2000-01-01', 'male'),
    ('petar@gmail.com', 'petar', '123321', '2000-02-02', 'male'),
    ('yasen@gmail.com', 'yasen', '123321', '2000-03-03', 'male'),
    ('alice@gmail.com', 'alice', '123321', '2000-04-04', 'female'),
    ('emma@gmail.new_usercom', 'emma', '123321', '2000-05-05', 'female'),
    ('oliver@gmail.com', 'oliver', '123321', '2000-06-06', 'male'),
    ('noah@gmail.com', 'noah', '123321', '2000-07-07', 'male'),
    ('lucas@gmail.com', 'lucas', '123321', '2000-08-08', 'male'),
    ('mia@gmail.com', 'mia', '123321', '2000-09-09', 'female'),
    ('sophia@gmail.com', 'sophia', '123321', '2000-10-10', 'female'),
    ('liam@gmail.com', 'liam', '123321', '2000-11-11', 'male'),
    ('charlotte@gmail.com', 'charlotte', '123321', '2000-12-12', 'female'),
    ('harry@gmail.com', 'harry', '123321', '2001-01-01', 'male'),
    ('olivia@gmail.com', 'olivia', '123321', '2001-02-02', 'female'),
    ('william@gmail.com', 'william', '123321', '2001-03-03', 'male');
-- -----------------------------------------------------------------------------



-- 3. TOPICS
-- 3.1. FITNESS
INSERT INTO new_forum_project.new_topic (title, topic_text, date_of_creation, category_name_of_category, id_of_author, best_reply_id)
VALUES ('Cardio vs. Strength', "I'm trying to decide between cardio and strength training. What's more effective for weight loss?", '2023-1-12', 'Fitness', 1, null),
       ('Healthy Diet Tips', "A balanced diet is crucial for fitness. What are your go-to healthy meals?", '2023-2-18', 'Fitness', 2, null),
       ('Best Home Workouts', "What are your favorite home workouts? Share some effective routines!", '2023-3-2', 'Fitness', 3, null),
       ('Muscle Building', "What's your preferred muscle-building routine? Share your exercises and tips!", '2023-4-8', 'Fitness', 4, null),
       ('Weight Loss Journeys', "Anyone here on a weight loss journey? Let's share progress and support each other.", '2023-9-21', 'Fitness', 5, null);

-- 3.2. FOOTBALL
INSERT INTO new_forum_project.new_topic (title, topic_text, date_of_creation, category_name_of_category, id_of_author, best_reply_id)
VALUES ('Champions League Predictions', "Who's your favorite to win the Champions League this season?", '2022-1-12', 'Football', 6, null),
       ('VAR Controversies', "VAR decisions lately have been controversial. What's your take?", '2022-2-12', 'Football', 7, null),
       ('Favorite Team Jerseys', "My favorite team jersey has to be Barcelona's home kit. Classic stripes!", '2022-3-9', 'Football', 8, null),
       ('Best Football Moments', "One of my best football moments was witnessing my favorite team winning the league title!", '2022-4-4', 'Football', 9, null),
       ('Youth Soccer Development', "What are the key aspects in youth soccer development? Coaching tips?", '2022-9-22', 'Football', 10, null);

-- 3.3. VOLLEYBALL
INSERT INTO new_forum_project.new_topic (title, topic_text, date_of_creation, category_name_of_category, id_of_author, best_reply_id)
VALUES ('Beach Volleyball Tips', "Any tips for playing beach volleyball? I'm new to it.", '2021-1-12', 'Volleyball', 11, null),
       ('Team Strategy Talks', "What's your favorite team strategy? I'm curious about different approaches.", '2021-6-12', 'Volleyball', 12, null),
       ('Indoor vs. Beach Volley', "Indoor or beach volleyball? Which one do you prefer and why?", '2021-4-9', 'Volleyball', 13, null),
       ('Blocking Techniques', "What are your favorite blocking techniques in soccer?", '2021-5-4', 'Volleyball', 14, null),
       ('Volleyball Injuries', "Dealing with a volleyball injury, any recovery tips?", '2021-8-22', 'Volleyball', 15, null);
-- -----------------------------------------------------------------------------




-- 4. REPLIES
-- 4.1. FITNESS
-- 4.1.1 "Cardio vs. Strength" ID: 1
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("Both are important, but diet plays a key role. Strength training builds muscle, which burns more calories at rest.", 1, 2),
       ("Cardio is great for burning calories during the activity. It also improves heart health and endurance.", 1, 6),
       (" For weight loss, consider a combination of both. Strength training 2-3 times a week, with regular cardio.", 1, 12),
       ("Diet is crucial. You can't out-exercise a bad diet. Balance cardio and strength, and watch your nutrition.", 1, 11),
       ("Remember, it's about what you enjoy. Choose a mix that keeps you motivated and consistent.", 1, 2);

-- 4.1.2 "Healthy Diet Tips" ID: 2
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("What's your favorite post-workout snack for refueling and staying on track", 2, 3),
       ("Let's discuss the role of hydration in maintaining a healthy diet for fitness.", 2, 2),
       ("Share your top tips for meal planning and prepping in your fitness journey.", 2, 3),
       ("What are some must-avoid foods when striving for a healthy, fit lifestyle?", 2, 4),
       ("How do you handle cravings for unhealthy foods while maintaining your diet?", 2, 6);

-- 4.1.3 "Best Home Workouts" ID: 3
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("I'm looking for home workout equipment recommendations. Any suggestions?", 3, 4),
       ("How do you stay motivated to work out at home consistently?", 3, 5),
       ("Let's discuss the benefits of home workouts, like saving time and money.", 3, 6),
       ("Share your success stories with home workouts and your progress.", 3, 7);

-- 4.1.4 "Muscle Building" ID: 4
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("How important is nutrition for muscle growth? Let's discuss meal plans.", 4, 5),
       ("Any favorite supplements for muscle building? Share your recommendations.", 4, 6),
       ("What's your experience with progressive overload in muscle-building programs?", 4, 9),
       ("Let's talk about recovery strategies after intense muscle-building workouts.", 4, 8),
       ("Share your success stories about transforming your physique through muscle building.", 4, 12);

-- 4.1.5 "Weight Loss Journeys" ID: 5
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("What's your favorite form of exercise for shedding pounds? Share your experiences.", 5, 8),
       ("How do you handle cravings during your weight loss journey? Tips are welcome!", 5, 15),
       ("Let's discuss the importance of a balanced diet for sustainable weight loss.", 5, 12),
       ("Share your success stories or obstacles you've overcome in your weight loss journey.", 5, 14);


-- 4.2. FOOTBALL
-- 4.2.1 "Cardio vs. Strength" ID: 6
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("Predictions for top goal scorer in the tournament? Share your thoughts.", 6, 7),
       ("Which underdog team do you think might surprise us in the Champions League?", 6, 12),
       ("Discuss key matchups or potential upsets in the upcoming Champions League games.", 6, 13),
       ("Share your thoughts on which team will lift the trophy this year. Let's hear your predictions!", 6, 12);

-- 4.2.2 "VAR Controversies" ID: 7
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("Share your views on how VAR can be improved in football.", 7, 8),
       ("Discuss specific incidents where VAR got it right or wrong.", 7, 5),
       ("Is VAR impacting the flow of the game too much? Let's debate.", 7, 3),
       ("What's your opinion on using VAR for offside calls in close situations?", 7, 6);

-- 4.2.3 "Favorite Team Jerseys" ID: 8
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("I'm a fan of the Liverpool away jersey. That shade of red is just fantastic.", 8, 9),
       ("As a Manchester United supporter, the '99 Treble-winning kit will always be special.", 8, 11),
       ("The Juventus black and white stripes are iconic. Love their jersey design.", 8, 2),
       ("AC Milan's red and black is a timeless combination. It's my top pick.", 8, 9);

-- 4.2.4 "Best Football Moments" ID: 9
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("That's awesome! I'll never forget the last-minute goal that secured a comeback win for my team.", 9, 10),
       ("Watching a World Cup final in the stadium was a dream come true. The atmosphere was electrifying.", 9, 11),
       ("When my local club upset a much stronger opponent in a cup match, it felt like a movie moment.", 9, 2),
       ("The best moment for me was when my kid scored their first goal in a youth league. Priceless!", 9, 13);

-- 4.2.5 "Youth Soccer Development" ID: 10
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("Focus on fundamentals: passing, dribbling, and teamwork. Patience and positive feedback are key.", 10, 11),
       ("Building confidence in young players is vital. Encourage creativity and a love for the game.", 10, 12),
       ("Small-sided games help improve skills and decision-making. Keep it fun to retain their interest.", 10, 1),
       ("Balance is crucial – develop skills, but don't forget about character building and sportsmanship.", 10, 9);


-- 4.3. VOLLEYBALL
-- 4.3.1 "Beach Volleyball Tips" ID: 11
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("Footwork is crucial on sand. Focus on positioning and communication with your partner.", 11, 12),
       ("Serving low and deep can be effective. The wind can affect the ball, so practice in different conditions.", 11, 2),
       ("Remember to stay hydrated and wear sunscreen. The sun can be intense on the beach!", 11, 6),
       ("Mental toughness is key. Stay positive, support your partner, and enjoy the unique beach volleyball experience.", 11, 8);

-- 4.3.2 "Team Strategy Talks" ID: 12
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("I prefer possession-based play. It's all about control and patience on the field.", 12, 13),
       ("Counter-attacking suits my team. Quick transitions catch opponents off guard.", 12, 15),
       ("High pressing is our style. We disrupt opponents' buildup and create chances.", 12, 1),
       ("Defending deep and hitting on the break works well for us. Compact and lethal on the counter.", 12, 8);

-- 4.3.3 "Indoor vs. Beach Volley" ID: 13
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("I like the challenge of beach volleyball. The sand adds a unique dimension to the game.", 13, 14),
       ("Indoor is my choice. The controlled environment allows for more precise plays.", 13, 1),
       ("Beach volleyball's casual vibe and natural surroundings make it my favorite.", 13, 7),
       ("Indoor for me. The speed and tactics suit my style better. Plus, no worries about weather!", 13, 3);

 -- 4.3.4 "Blocking Techniques" ID: 14
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("I prefer jockeying. It's all about positioning and timing to block the passing lanes.", 14, 15),
       ("Sliding tackles are my go-to. Effective when executed correctly.", 14, 3),
       ("I use the 'Contain and Block' method. It reduces the risk of getting beaten.", 14, 1),
       ("Pressing high and intercepting passes is my way to block the opponent's play.", 14, 2);

 -- 4.3.5 "Volleyball Injuries" ID: 15
INSERT INTO new_forum_project.replies (text, new_topic_id, new_user_id)
VALUES ("Rest is crucial. Follow a physio's plan and don't rush back.", 15, 1),
       ("Strengthen your muscles to prevent future injuries. It's key.", 15, 12),
       ("Ice and elevate for swelling. And wear protective gear to avoid injuries.", 15, 2),
       ("Listen to your body. If pain persists, seek professional medical advice. Safety first.", 15, 13);
-- -----------------------------------------------------------------------------




-- 5. CONVERSATION
-- 5.1 conversation # 1
INSERT INTO new_forum_project.conversations (id_of_conversations, the_receiver, the_sender)
VALUES (1, 1, 2);

-- 5.2 conversation # 2
INSERT INTO new_forum_project.conversations (id_of_conversations, the_receiver, the_sender)
VALUES (2, 1, 3);

-- 5.3 conversation # 3
INSERT INTO new_forum_project.conversations (id_of_conversations, the_receiver, the_sender)
VALUES (3, 2, 1);

-- 5.4 conversation # 4
INSERT INTO new_forum_project.conversations (id_of_conversations, the_receiver, the_sender)
VALUES (4, 2, 3);

-- 5.5 conversation # 5
INSERT INTO new_forum_project.conversations (id_of_conversations, the_receiver, the_sender)
VALUES (5, 3, 1);

-- 5.6 conversation # 6
INSERT INTO new_forum_project.conversations (id_of_conversations, the_receiver, the_sender)
VALUES (6, 3, 2);
-- -----------------------------------------------------------------------------



-- 6. MESSAGES
-- 6.1 chat # 1
INSERT INTO new_forum_project.messages (text_message, conversation_id, the_sender)
VALUES ("Hey! How's your fitness routine going?", 1, 1),
       ("Hi! It's been great. I'm hitting the gym regularly.", 1, 2),
       ("That's awesome! What's your favorite workout these days?", 1, 1),
       ("I'm really into HIIT workouts and weightlifting.", 1, 2);

-- 6.2 chat # 2
INSERT INTO new_forum_project.messages (text_message, conversation_id, the_sender)
VALUES ("Hi there! How's your fitness journey shaping up?", 2, 1),
       ("Hey! It's been quite the journey. I'm loving it!", 2, 3),
       ("Excellent! Any tips on staying motivated?", 2, 1),
       ("Setting specific goals and tracking progress really helps.", 2, 3);

-- 6.3 chat # 3
INSERT INTO new_forum_project.messages (text_message, conversation_id, the_sender)
VALUES ("Hello! What's new in your fitness routine?", 3, 2),
       ("Hey! I've been trying some new yoga routines lately.", 3, 1),
       ("That's interesting! How do you find it so far?", 3, 2),
       ("It's been great for flexibility and relaxation.", 3, 1),
       ("Yoga can be an amazing addition to any fitness regimen.", 3, 2);

-- 6.4 chat # 4
INSERT INTO new_forum_project.messages (text_message, conversation_id, the_sender)
VALUES ("Hey, how's your football season going?", 4, 2),
       ("Hi! It's been good. Our team is performing well.", 4, 3),
       ("That's great to hear! Any standout moments?", 4, 2),
       ("Yeah, I scored a hat-trick last week!", 4, 3);

-- 6.5 chat # 5
INSERT INTO new_forum_project.messages (text_message, conversation_id, the_sender)
VALUES ("Hi there! How's your soccer training these days", 5, 3),
       ("Hey! It's intense, but I'm loving it.", 5, 1),
       ("Any particular skills or drills you're focusing on?", 5, 3),
       ("Dribbling and passing accuracy are my priorities.", 5, 1);

-- 6.6 chat # 6
INSERT INTO new_forum_project.messages (text_message, conversation_id, the_sender)
VALUES ("Hello! Have you been watching any football matches recently?", 6, 3),
       ("Hi! Yes, I watched the big game last night.", 6, 2),
       ("How did it go? Any surprising results?", 6, 3),
       ("It was a draw, but the underdog team played really well.", 6, 2);
-- -----------------------------------------------------------------------------




-- 7. REACTIONS_OF_REPLIES
INSERT INTO new_forum_project.reactions_of_replies (UpVote, DownVote, new_user_id, id_of_replies)
VALUES (1, 0, 1, 1),
       (1, 0, 2, 1),
       (1, 0, 3, 1),
       (0, 1, 4, 1),
       (1, 0, 5, 2),
       (1, 0, 5, 2),
       (0, -1, 6, 2),
       (1, 0, 6, 3),
       (1, 0, 7, 3),
       (1, 0, 8, 4),
       (1, 0, 4, 4),
       (0, -1, 5, 4),
       (1, 0, 2, 5),
       (1, 0, 15, 6),
       (1, 0, 14, 7),
       (1, 0, 13, 7),
       (0, -1, 12, 7),
       (1, 0, 2, 8),
       (1, 0, 8, 11),
       (1, 0, 7, 11),
       (1, 0, 7, 12),
       (1, 0, 5, 13),
       (1, 0, 3, 14),
       (0, -1, 1, 16),
       (1, 0, 10, 16),
       (1, 0, 10, 17),
       (1, 0, 10, 18),
       (1, 0, 15, 18),
       (1, 0, 15, 19),
       (1, 0, 12, 20),
       (0, -1, 14, 20),
       (1, 0, 1, 20),
       (1, 0, 1, 22),
       (1, 0, 2, 22),
       (1, 0, 3, 24),
       (0, -1, 3, 26),
       (1, 0, 8, 26),
       (1, 0, 7, 27),
       (1, 0, 5, 28),
       (1, 0, 6, 28),
       (0, -1, 14, 28),
       (1, 0, 15, 30),
       (1, 0, 12, 30),
       (1, 0, 8, 31),
       (1, 0, 9, 31),
       (1, 0, 9, 32),
       (0, -1, 9, 33),
       (1, 0, 4, 35),
       (1, 0, 4, 35),
       (1, 0, 9, 37),
       (1, 0, 11, 37),
       (1, 0, 15, 37),
       (1, 0, 7, 38),
       (0, -1, 8, 38),
       (0, -1, 5, 38),
       (0, -1, 6, 40),
       (1, 0, 3, 40),
       (1, 0, 12, 42),
       (1, 0, 13, 44),
       (1, 0, 11, 44),
       (1, 0, 7, 44),
       (1, 0, 6, 45),
       (0, -1, 3, 45),
       (1, 0, 3, 46),
       (0, -1, 4, 46),
       (1, 0, 1, 47),
       (1, 0, 2, 48),
       (1, 0, 3, 49),
       (1, 0, 3, 49),
       (1, 0, 4, 51),
       (1, 0, 4, 51),
       (1, 0, 5, 52),
       (1, 0, 6, 53),
       (1, 0, 6, 53),
       (1, 0, 7, 54),
       (1, 0, 8, 56),
       (1, 0, 8, 56),
       (1, 0, 9, 57),
       (1, 0, 9, 57),
       (1, 0, 11, 58),
       (1, 0, 10, 58),
       (1, 0, 12, 58),
       (1, 0, 11, 59),
       (1, 0, 13, 59),
       (1, 0, 1, 59),
       (1, 0, 1, 60),
       (1, 0, 13, 61),
       (1, 0, 14, 61),
       (1, 0, 15, 61),
       (0, -1, 13, 61),
       (1, 0, 8, 61),
       (1, 0, 7, 61),
       (0, -1, 6, 62),
       (1, 0, 5, 62),
       (1, 0, 4, 62),
       (1, 0, 1, 62);
-- -----------------------------------------------------------------------------

