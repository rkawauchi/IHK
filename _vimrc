set nocompatible
source $VIMRUNTIME/vimrc_example.vim
source $VIMRUNTIME/mswin.vim
behave mswin

set winaltkeys=no

"For Vundle (not working, fix when have time)
"filetype off
"set rtp+=~/.vim/bundle/vundle/
"call vundle#rc()
"Bundle 'gmarik/vundle'

"Paste with proper indentation
"noremap p p=<Right>

"Force typical Windows bindings
nmap <C-s> :w<Enter>
imap <C-s> <C-o>:w<Enter>
nmap <C-z> u
imap <C-z> <C-o>u
"this doesn't work properly. need to figure out how <C-r> works.
"map <C-y> <C-r>
nmap <C-v> "*p
imap <C-v> <C-r>*

"Change font
if has("gui_running")
  if has("gui_gtk2")
    set guifont=Inconsolata\ 12
  elseif has("gui_macvim")
    set guifont=Menlo\ Regular:h14
  elseif has("gui_win32")
    set guifont=Consolas:h12:cANSI
  endif
endif

set diffexpr=MyDiff()
function MyDiff()
  let opt = '-a --binary '
  if &diffopt =~ 'icase' | let opt = opt . '-i ' | endif
  if &diffopt =~ 'iwhite' | let opt = opt . '-b ' | endif
  let arg1 = v:fname_in
  if arg1 =~ ' ' | let arg1 = '"' . arg1 . '"' | endif
  let arg2 = v:fname_new
  if arg2 =~ ' ' | let arg2 = '"' . arg2 . '"' | endif
  let arg3 = v:fname_out
  if arg3 =~ ' ' | let arg3 = '"' . arg3 . '"' | endif
  let eq = ''
  if $VIMRUNTIME =~ ' '
    if &sh =~ '\<cmd'
      let cmd = '""' . $VIMRUNTIME . '\diff"'
      let eq = '"'
    else
      let cmd = substitute($VIMRUNTIME, ' ', '" ', '') . '\diff"'
    endif
  else
    let cmd = $VIMRUNTIME . '\diff'
  endif
  silent execute '!' . cmd . ' ' . opt . arg1 . ' ' . arg2 . ' > ' . arg3 . eq
endfunction

" REQUIRED. This makes vim invoke Latex-Suite when you open a tex file.
filetype plugin on
" Also enable syntax
syntax enable

" IMPORTANT: win32 users will need to have 'shellslash' set so that latex
" can be called correctly.
set shellslash

" IMPORTANT: grep will sometimes skip displaying the file name if you
" search in a singe file. This will confuse Latex-Suite. Set your grep
" program to always generate a file-name.
set grepprg=grep\ -nH\ $*

" OPTIONAL: This enables automatic indentation as you type.
filetype indent on

" OPTIONAL: Starting with Vim 7, the filetype of empty .tex files defaults to
" 'plaintex' instead of 'tex', which results in vim-latex not being loaded.
" The following changes the default filetype back to 'tex':
let g:tex_flavor='latex'

" map control-backspace to delete the previous word (doesn't work)
imap <C-BS> <C-o>db
nmap <C-BS> db
nmap <C-Del> de

"deal with line breaks
set textwidth=80
set formatoptions=cq
set wrapmargin=0
set linebreak
command Nobreak set wrap|set textwidth=0|set wrapmargin=0
command Break set nowrap|set textwidth=80|set wrapmargin=0

"use mostly case insensitive search
:set ignorecase
:set smartcase

"Change backup file locations
set backupdir=./_backup,.,/tmp
set directory=.,./_backup,/tmp

"quicksearch
command -nargs=1 Sh noautocmd vim /<args>/ *
command -nargs=1 Sj noautocmd vim /<args>/j *|cw

"easier window navigation
noremap <M-w> <C-w>
noremap <M-w><M-w> <C-w>w
noremap <M-w><M-v> <C-w>v
noremap <M-w><M-s> <C-w>s
noremap <M-w><M-q> <C-w>q

"to search and replace easily. s is from current location in the file, S is full file
nmap s :.,$s:::cg<Left><Left><Left><Left>
nmap S :%s:::cg<Left><Left><Left><Left>
"fix accidental lack of saving
nmap s<C-s> <C-s>
"replace current word. The word is placed into the s register for ease of access.
nmap s* "syiw:.,$s:<C-r>s::cg<Left><Left><Left>
nmap S* "syiw:%s:<C-r>s::cg<Left><Left><Left>
"nnoremap ;c :.,s:::gn<Left><Left><Left><Left>
"no confirmation
"nmap S :.,s:::g<Left><Left><Left>
"nmap S* "9yiw:.,$s:<C-r>9::g<Left><Left>

"Regex stuff
noremap .*? .\{-}

"Use arrow keys properly in wrapped lines
imap <silent> <Down> <C-o>gj
imap <silent> <Up> <C-o>gk
imap <silent> <End> <C-o>g<End>
vmap <silent> <Down> <C-o>gj
vmap <silent> <Up> <C-o>gk
vmap <silent> <End> <C-o>g<End>
nmap <silent> <Down> gj
nmap <silent> <Up> gk
map <silent> <End> g<End>
"Use 'soft' home (doesn't work well with multiline stuff)
"Potentially enable only for "coding" files?
"Or disable only for .txt and similar files?
inoremap <silent> <home> <C-o>_
vnoremap <silent> <home> <C-o>_
noremap <silent> <home> _
noremap <silent> _ g<home>
"Use multiline friendly home on other file types
autocmd Filetype text,tex imap <silent> <home> <C-o>g<home>
autocmd Filetype text,tex vmap <silent> <home> <C-o>g<home>
autocmd Filetype text,tex map <silent> <home> g<home>

"Easier deletion
noremap dd dd<Right>
noremap dw daw
noremap di dawi
nmap ds d/

"paste on next line
nmap P o<Esc>p

"use ' to go to the mark directly and ` to go to the beginning of the line
noremap ' `
noremap ` '

"Replace tabs
set tabstop=4
set shiftwidth=4
set expandtab

"Remove annoying backup files
set nobackup
set nowritebackup
set noswapfile

"Change color scheme
"colo vibrantink this has weird highlighting
colo blacksea

"Tabbing
nmap <S-Tab> <<
"nmap <Tab> >>
imap <S-Tab> <Esc><<i

"HTML tabs
autocmd FileType html setlocal shiftwidth=2 tabstop=2

"Run external commands
nmap ! :!
nmap !! :!<Up><Enter>

"Allow true quotes in bib files
autocmd Filetype bib inoremap " <C-Q>"

"remove markers in vim latex
let g:Imap_UsePlaceHolders = 0

"Way to quickly exit insert mode
imap ii <Esc><Right>

"search files quickly
noremap <C-f> <C-c>:noautocmd vimgrep  **/*.py **/*.js **/*.html **/*.css<Home><C-Right><C-Right><Right>

"Navigate ctags tree
map <C-[> <C-t>
"Run ctags on save
"need to figure out how to make it work with javascript, exclude libraries
autocmd BufWritePost *.py,*.tex silent! !ctags -R

"connect z functions to normal arrow navigation
nmap zi zt
nmap zk zb

"more consistent Ctrl-R
nmap <C-r> i<C-r>

"insert single character quickly
"http://stackoverflow.com/questions/1764263/what-is-the-leader-in-a-vimrc-file
nmap <Space> i_<Esc>r
nnoremap <S-Space> s

"yank to end of line, consistent with D
nmap Y y$

"compatibility with ConEmu hack
imap zii <Esc><Right>
nmap ziidbi db

"ignore file types when doing tab completion
set wildignore=*.aux,*.pyc,*.log,*.pptx,*.pdf,*.blg

"Grab sentences quickly
map d. T.<Right>df.
map y. T.<Right>yf.

"don't beep
set visualbell
set noerrorbells

"show line numbers
"set number

"enable backspacing over everything in indent mode
set backspace=indent,eol,start

"search better
set hlsearch
set incsearch

"Screen navigation
noremap n nzz
noremap N Nzz
noremap <PageDown> <C-d>
noremap <PageUp> <C-u>
"map <PageDown> :set scroll=0<CR>:set scroll^=2<CR>:set scroll-=1<CR><C-D>:set scroll=0<CR>
"map <PageUp> :set scroll=0<CR>:set scroll^=2<CR>:set scroll-=1<CR><C-U>:set scroll=0<CR>

"Insert at end of word
nmap I ei<Right>