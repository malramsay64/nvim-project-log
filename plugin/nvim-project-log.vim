nnoremap <space>l :ProjectLogToday<CR>
nnoremap <space>i :ProjectLogIndex<CR>
nnoremap <down> :ProjectLogPrevious<CR>
nnoremap <up> :ProjectLogNext<CR>
nnoremap <space>gi :ProjectLogUpdateIndex<CR>

if !exists("g:project_log#log_level")
    let g:project_log#log_level = 'INFO'
endif
