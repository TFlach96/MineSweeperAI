;source code from
;https://rosettacode.org/wiki/Minesweeper_game
(defclass minefield ()
  ((mines :initform (make-hash-table :test #'equal))
   (width :initarg :width)
   (height :initarg :height)
   (grid :initarg :grid)))
 
(defun make-minefield (width height num-mines)
  (let ((minefield (make-instance 'minefield
                                  :width width
                                  :height height
                                  :grid (make-array
                                          (list width height)
                                          :initial-element #\.)))
        (mine-count 0))
    (with-slots (grid mines) minefield
      (loop while (< mine-count num-mines)
            do (let ((coords (list (random width) (random height))))
                 (unless (gethash coords mines)
                   (setf (gethash coords mines) T)
                   (incf mine-count))))
      minefield)))
 
(defun print-field (minefield)
  (with-slots (width height grid) minefield
    (dotimes (y height)
      (dotimes (x width)
        (princ (aref grid x y)))
      (format t "~%"))))
 
(defun mine-list (minefield)
  (loop for key being the hash-keys of (slot-value minefield 'mines) collect key))

(defun adjacent-clear (minefield coords)
  (with-slots (width height grid) minefield
    (dotimes (y height)
      (dotimes (x width)
        (let ((adjCoords (list x y))) 
          (when ;if the x and y loop are withing 1 space of the coordinates
            (and
              (> 2 (abs (- (car coords) x)))
              (> 2 (abs (- (cadr coords) y)))
            )
              (clear minefield adjCoords) ;clear the adjacent location
          )
        )
      )
    )
    (setf (aref grid (car coords) (cadr coords)) (aref grid (car coords) (cadr coords)))
  )
)
 
(defun count-nearby-mines (minefield coords)
  (length (remove-if-not
            (lambda (mine-coord)
              (and
                (> 2 (abs (- (car coords) (car mine-coord))))
                (> 2 (abs (- (cadr coords) (cadr mine-coord))))))
            (mine-list minefield))))
 
(defun clear (minefield coords)
  (with-slots (mines grid) minefield
    (if (or (equalp (aref grid (car coords) (cadr coords)) #\.) (equalp (aref grid (car coords) (cadr coords)) #\?)) ;If coords have not already been cleared or is marked, continue.
      (if (gethash coords mines)
        (progn
          (format t "MINE! You lose.~%")
          (dolist (mine-coords (mine-list minefield))
            (setf (aref grid (car mine-coords) (cadr mine-coords)) #\x))
          (setf (aref grid (car coords) (cadr coords)) #\X)
          nil)
        (let ((x (count-nearby-mines minefield coords))) ;store the number of adjacent mines in x
          (setf (aref grid (car coords) (cadr coords))
              (elt "0123456789" x))
          (if (eql x 0) ;if no mines clear adjacent areas recursively.
            (adjacent-clear minefield coords) 
            (setf (aref grid (car coords) (cadr coords)) (aref grid (car coords) (cadr coords))))))
      ;else ignore and set to itself
      (setf (aref grid (car coords) (cadr coords)) (aref grid (car coords) (cadr coords)))))) ;ignore this space but don't terminate
 
(defun mark (minefield coords)
  (with-slots (mines grid) minefield
    (setf (aref grid (car coords) (cadr coords)) #\?)))
 
(defun win-p (minefield)
  (with-slots (width height grid mines) minefield
    (let ((num-uncleared 0))
      (dotimes (y height)
        (dotimes (x width)
          (let ((square (aref grid x y)))
            (when (member square '(#\. #\?) :test #'char=)
              (incf num-uncleared)))))
      (= num-uncleared (hash-table-count mines)))))
 
(defun play-game ()
  (let ((minefield (make-minefield 8 8 8))) ;make-minefield col row mines
    (format t "Greetings player, there are ~a mines.~%"
            (hash-table-count (slot-value minefield 'mines)))
    (loop
      (print-field minefield)
      (format t "Enter your command, examples: \"clear 0 1\" \"mark 1 2\" \"quit\".~%")
      (princ "> ")
      (let ((user-command (read-from-string (format nil "(~a)" (read-line)))))
        (format t "Your command: ~a~%" user-command)
        (case (car user-command)
          (quit (return-from play-game nil))
          (clear (unless (clear minefield (cdr user-command))
                   (print-field minefield)
                   (return-from play-game nil)))
          (mark (mark minefield (cdr user-command))))
        (when (win-p minefield)
          (format t "Congratulations, you've won!")
          (return-from play-game T))))))
(defun return-true ()
t
  )
(defun return-false ()
nil
  )

(defparameter *col* 8)
(defparameter *row* 8)
(defparameter *mines* 8)
(defvar zerotiles '())
(defvar edgetiles '())
(defvar history '())
(defvar action '())

(defun inbounds (col row)
  (when (>= col 0)
    (when (< col *col*)
      (when (>= row 0)
        (when (< row *row*)
          (return-true)
          )
        )
      )
    )
  (return-false)
  )
                                        ;copy game, make subfunctions for DFS
(defun minesweeper-dfsai()
                       
                        (let ((minefield (make-minefield 8 8 8)) (moves 1) (firstmove (list (random *col*) (random *row*)))) ;make-minefield col row mines, moves for ai tracking, firstmove for ai
                          (loop
                           (print-field minefield)
                            (when ( = moves 1)
                              (clear minefield firstmove)
                              (print firstmove)
                              (terpri)
                              
                                )
                            (when (>= moves 2)
                              
                              )
                            (incf moves)
                          
                                )
                           
                            ))


                                        ;(play-game)
(minesweeper-dfsai)
